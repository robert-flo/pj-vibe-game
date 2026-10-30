import json
import os
import re
import struct
import subprocess
import wave
import numpy as np

R96_SOUND = "/home/omarchy/Projects/Render96ex/sound"
SEQ_DECODER = "/home/omarchy/Projects/Render96ex/tools/seq_decoder.py"
OUT_DIR = "/home/omarchy/Projects/pj-vibe-game/assets/audio/sm64"
os.makedirs(OUT_DIR, exist_ok=True)

OUT_SR = 32000


def parse_f80(data):
    exp_bits, mant = struct.unpack(">HQ", data)
    sign = -1.0 if (exp_bits & 0x8000) else 1.0
    exp_bits &= 0x7FFF
    if exp_bits == 0 and mant == 0:
        return 0.0
    return sign * (float(mant) / (2.0 ** 63)) * (2.0 ** (exp_bits - 0x3FFF))


_sample_cache = {}


def load_aiff(bank_dir, sample_name):
    key = (bank_dir, sample_name)
    if key in _sample_cache:
        return _sample_cache[key]
    path = os.path.join(R96_SOUND, "samples", bank_dir, f"{sample_name}.aiff")
    with open(path, "rb") as f:
        d = f.read()
    i = 12
    sr = 32000.0
    markers = {}
    loop_mode = 0
    begin_id = end_id = 0
    pcm = np.zeros(1, dtype=np.float32)
    while i < len(d):
        tp = d[i:i+4]
        sz, = struct.unpack(">I", d[i+4:i+8])
        body = d[i+8:i+8+sz]
        if tp == b"COMM":
            sr = parse_f80(body[8:18])
        elif tp == b"MARK":
            nm, = struct.unpack(">H", body[:2])
            p = 2
            for _ in range(nm):
                mid, mpos = struct.unpack(">HI", body[p:p+6])
                slen = body[p+6]
                p += 7 + slen + ((slen + 1) & 1 == 0 and 0 or 0)
                # Pascal string in AIFF: total bytes = 1 + slen, padded to even
                p = p - (7 + slen) + 6 + (((1 + slen) + 1) & -2)
                markers[mid] = mpos
        elif tp == b"INST":
            loop_mode, begin_id, end_id = struct.unpack(">hhh", body[8:14])
        elif tp == b"SSND":
            raw = body[8:]
            n = len(raw) // 2
            pcm = np.frombuffer(raw[:n*2], dtype=">i2").astype(np.float32) / 32768.0
        i += 8 + ((sz + 1) & -2)

    loop = None
    if loop_mode != 0 and begin_id in markers and end_id in markers:
        ls, le = markers[begin_id], markers[end_id]
        if 0 <= ls < le <= len(pcm):
            loop = (ls, le)
    res = (pcm, sr, loop)
    _sample_cache[key] = res
    return res


def load_bank(bank_name):
    path = os.path.join(R96_SOUND, "sound_banks", f"{bank_name}.json")
    with open(path, "r") as f:
        txt = re.sub(r"/\*.*?\*/", "", f.read(), flags=re.DOTALL)
        txt = re.sub(r"//.*?\n", "\n", txt)
        return json.loads(txt)


def synth_note(pcm, loop, step, on_samples, rel_samples, vol_l, vol_r):
    total = on_samples + rel_samples
    if total <= 0 or step <= 0:
        return np.zeros((0, 2), dtype=np.float32)
    idx = np.arange(total, dtype=np.float64) * step
    if loop is not None:
        ls, le = loop
        llen = max(1, le - ls)
        over = idx >= le
        if np.any(over):
            idx[over] = ls + np.mod(idx[over] - ls, llen)
    else:
        valid = idx < (len(pcm) - 1)
        if not np.all(valid):
            total = int(np.argmax(~valid))
            if total <= 0:
                return np.zeros((0, 2), dtype=np.float32)
            idx = idx[:total]
            on_samples = min(on_samples, total)
            rel_samples = total - on_samples

    i0 = idx.astype(np.int32)
    frac = (idx - i0).astype(np.float32)
    i1 = np.minimum(i0 + 1, len(pcm) - 1)
    wave_mono = pcm[i0] * (1.0 - frac) + pcm[i1] * frac

    env = np.ones(len(wave_mono), dtype=np.float32)
    atk = min(48, len(env))
    if atk > 1:
        env[:atk] = np.linspace(0.0, 1.0, atk, dtype=np.float32)
    if rel_samples > 0 and on_samples < len(env):
        rlen = len(env) - on_samples
        env[on_samples:] = np.linspace(1.0, 0.0, rlen, dtype=np.float32) ** 1.8

    wave_mono *= env
    out = np.empty((len(wave_mono), 2), dtype=np.float32)
    out[:, 0] = wave_mono * vol_l
    out[:, 1] = wave_mono * vol_r
    return out


def save_mp3(stereo_buf, mp3_path, fade_out_s=0.0):
    if fade_out_s > 0:
        fn = min(int(fade_out_s * OUT_SR), len(stereo_buf))
        if fn > 0:
            fade = np.linspace(1.0, 0.0, fn, dtype=np.float32)[:, None]
            stereo_buf[-fn:] *= fade
    peak = float(np.max(np.abs(stereo_buf))) if len(stereo_buf) else 1.0
    if peak > 1e-5:
        stereo_buf = stereo_buf * (0.90 / peak)
    pcm16 = np.clip(stereo_buf * 32767.0, -32768, 32767).astype("<i2")
    tmp_wav = "/tmp/sm64_tmp.wav"
    with wave.open(tmp_wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(OUT_SR)
        wf.writeframes(pcm16.tobytes())
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_wav, "-b:a", "160k", mp3_path],
        check=True,
    )
    os.remove(tmp_wav)
    print(f"Saved {mp3_path} ({len(stereo_buf)/OUT_SR:.2f}s)")


def parse_int(tok):
    return int(tok.strip(), 0)


def render_m64(m64_name, bank_name, out_mp3, max_loops=1, fade_out_s=0.0):
    m64_path = os.path.join(R96_SOUND, "sequences", "us", m64_name)
    asm = subprocess.check_output(["python3", SEQ_DECODER, m64_path], text=True)
    bank = load_bank(bank_name)
    sbank_dir = bank["sample_bank"]
    inst_list = bank["instrument_list"]
    instruments = bank["instruments"]

    lines = [l.strip() for l in asm.splitlines() if l.strip() and not l.strip().startswith(("#", ".include", ".section", ".align"))]
    labels = {}
    for idx, l in enumerate(lines):
        if l.endswith(":"):
            labels[l[:-1]] = idx

    def parse_args(line):
        parts = line.split(None, 1)
        op = parts[0]
        args = [a.strip() for a in parts[1].split(",")] if len(parts) > 1 else []
        return op, args

    # Collect note events by simulating ticks
    tempo = 120
    seq_vol = 100
    pc = labels.get("sequence_start", 0) + 1
    seq_delay = 0
    jumps_taken = 0

    channels = {}
    active_layers = {}
    note_events = []  # (start_sec, on_sec, rel_sec, inst_id, semitone, vel, pan, cvol, pitchbend)

    cur_time = 0.0
    max_ticks = 40000

    for _tick in range(max_ticks):
        # Advance sequence script when seq_delay == 0
        while seq_delay <= 0 and pc < len(lines):
            l = lines[pc]
            pc += 1
            if l.endswith(":") or l.startswith(".byte"):
                continue
            op, args = parse_args(l)
            if op == "seq_settempo":
                tempo = max(1, parse_int(args[0]))
            elif op == "seq_setvol":
                seq_vol = parse_int(args[0])
            elif op == "seq_startchannel":
                cid = parse_int(args[0])
                lbl = args[1]
                channels[cid] = {
                    "pc": labels[lbl] + 1,
                    "delay": 0,
                    "instr": 0,
                    "vol": 127,
                    "pan": 64,
                    "transpose": 0,
                    "pb": 0,
                    "active": True,
                }
            elif op == "seq_disablechannels":
                mask = parse_int(args[0])
                for cid in list(channels.keys()):
                    if mask & (1 << cid):
                        channels[cid]["active"] = False
            elif op == "seq_delay":
                seq_delay = parse_int(args[0])
            elif op == "seq_delay1":
                seq_delay = 1
            elif op == "seq_jump":
                jumps_taken += 1
                if jumps_taken >= max_loops:
                    pc = len(lines)
                    break
                pc = labels[args[0]] + 1
            elif op == "seq_end":
                pc = len(lines)
                break

        if pc >= len(lines) and seq_delay <= 0:
            break

        dt = 60.0 / (tempo * 48.0)

        # Advance active channels
        for cid, ch in list(channels.items()):
            if not ch["active"]:
                continue
            while ch["delay"] <= 0 and ch["pc"] < len(lines):
                l = lines[ch["pc"]]
                ch["pc"] += 1
                if l.endswith(":"):
                    continue
                op, args = parse_args(l)
                if op == "chan_setinstr":
                    ch["instr"] = parse_int(args[0])
                elif op == "chan_setvol":
                    ch["vol"] = parse_int(args[0])
                elif op == "chan_setpan":
                    ch["pan"] = parse_int(args[0])
                elif op == "chan_transpose":
                    v = parse_int(args[0])
                    ch["transpose"] = v - 256 if v > 127 else v
                elif op == "chan_pitchbend":
                    v = parse_int(args[0])
                    ch["pb"] = v - 256 if v > 127 else v
                elif op == "chan_setlayer":
                    lid = parse_int(args[0])
                    lbl = args[1]
                    active_layers[(cid, lid)] = {
                        "pc": labels[lbl] + 1,
                        "delay": 0,
                        "last_delay": 24,
                        "transpose": 0,
                        "stack": [],
                        "active": True,
                        "instr_override": None,
                    }
                elif op == "chan_delay":
                    ch["delay"] = parse_int(args[0])
                elif op == "chan_delay1":
                    ch["delay"] = 1
                elif op in ("chan_end", "chan_hang"):
                    ch["delay"] = 999999
                    break
            ch["delay"] -= 1

        # Advance active layers
        for (cid, lid), ly in list(active_layers.items()):
            ch = channels.get(cid)
            if not ly["active"] or not ch or not ch["active"]:
                continue
            while ly["delay"] <= 0 and ly["pc"] < len(lines):
                l = lines[ly["pc"]]
                ly["pc"] += 1
                if l.endswith(":"):
                    continue
                op, args = parse_args(l)
                if op == "layer_delay":
                    ly["delay"] = parse_int(args[0])
                elif op == "layer_transpose":
                    v = parse_int(args[0])
                    ly["transpose"] = v - 256 if v > 127 else v
                elif op == "layer_setinstr":
                    ly["instr_override"] = parse_int(args[0])
                elif op == "layer_call":
                    ly["stack"].append(ly["pc"])
                    ly["pc"] = labels[args[0]] + 1
                elif op == "layer_jump":
                    ly["pc"] = labels[args[0]] + 1
                elif op == "layer_end":
                    if ly["stack"]:
                        ly["pc"] = ly["stack"].pop()
                    else:
                        ly["active"] = False
                        break
                elif op in ("layer_note0", "layer_note1", "layer_note2"):
                    semi = parse_int(args[0])
                    if op == "layer_note0":
                        ndelay = parse_int(args[1])
                        vel = parse_int(args[2])
                        ndur = parse_int(args[3])
                        ly["last_delay"] = ndelay
                    elif op == "layer_note1":
                        ndelay = parse_int(args[1])
                        vel = parse_int(args[2])
                        ndur = 0
                        ly["last_delay"] = ndelay
                    else:
                        ndelay = ly["last_delay"]
                        vel = parse_int(args[1])
                        ndur = parse_int(args[2])
                    ly["delay"] = ndelay
                    off_ticks = (ndur * ndelay) // 256
                    on_ticks = max(1, ndelay - off_ticks)
                    inst_id = ly["instr_override"] if ly["instr_override"] is not None else ch["instr"]
                    note_events.append((
                        cur_time,
                        on_ticks * dt,
                        inst_id,
                        semi + ch["transpose"] + ly["transpose"],
                        vel,
                        ch["pan"],
                        (ch["vol"] / 127.0) * (seq_vol / 127.0),
                        ch["pb"],
                    ))
            ly["delay"] -= 1

        seq_delay -= 1
        cur_time += dt

    total_samples = int((cur_time + 1.5) * OUT_SR)
    mix = np.zeros((total_samples, 2), dtype=np.float32)

    for t0, on_sec, inst_id, semi, vel, pan, cvol, pb in note_events:
        s0 = int(t0 * OUT_SR)
        if s0 >= total_samples:
            continue
        is_drum = (inst_id == 0x7F)
        snd_obj = None
        rel_rate = 208
        if is_drum:
            drums = instruments.get("percussion", [])
            if 0 <= semi < len(drums):
                dentry = drums[semi]
                snd_obj = dentry["sound"]
                rel_rate = dentry.get("release_rate", 10)
                pan = dentry.get("pan", pan)
        else:
            if 0 <= inst_id < len(inst_list) and inst_list[inst_id]:
                ientry = instruments[inst_list[inst_id]]
                rel_rate = ientry.get("release_rate", 208)
                lo = ientry.get("normal_range_lo", 0)
                hi = ientry.get("normal_range_hi", 127)
                if semi < lo and "sound_lo" in ientry:
                    snd_obj = ientry["sound_lo"]
                elif semi > hi and "sound_hi" in ientry:
                    snd_obj = ientry["sound_hi"]
                else:
                    snd_obj = ientry["sound"]

        if snd_obj is None:
            continue
        if isinstance(snd_obj, str):
            sname, tuning = snd_obj, None
        else:
            sname, tuning = snd_obj["sample"], snd_obj.get("tuning", None)

        pcm, sr, loop = load_aiff(sbank_dir, sname)
        if tuning is None:
            tuning = sr / float(OUT_SR)

        if is_drum:
            step = tuning
        else:
            pb_semi = (pb / 127.0) * 2.0
            step = (2.0 ** ((semi + pb_semi - 39.0) / 12.0)) * tuning

        on_samps = max(1, int(on_sec * OUT_SR))
        rel_sec = min(0.45, max(0.03, (255 - min(250, rel_rate)) / 420.0))
        rel_samps = int(rel_sec * OUT_SR)

        gain = (vel / 127.0) * cvol * 0.35
        pan_f = np.clip(pan / 127.0, 0.0, 1.0)
        vol_l = gain * np.cos(pan_f * np.pi * 0.5)
        vol_r = gain * np.sin(pan_f * np.pi * 0.5)

        w = synth_note(pcm, loop, step, on_samps, rel_samps, vol_l, vol_r)
        end = min(total_samples, s0 + len(w))
        if end > s0:
            mix[s0:end] += w[:end - s0]

    save_mp3(mix, os.path.join(OUT_DIR, out_mp3), fade_out_s=fade_out_s)


# 1. Classic SM64 Star / Victory Fanfare
render_m64("01_cutscene_collect_star.m64", "22", "star_fanfare.mp3", max_loops=1, fade_out_s=0.25)

# 2. Classic SM64 Outdoor Main Theme BGM (1 full intro + loop, smooth loop tail)
render_m64("03_level_grass.m64", "22", "castle_grounds_bgm.mp3", max_loops=1, fade_out_s=0.8)

# 3. Authentic Coin SFX (.sound_general_coin: sfx_9/03.aiff, transpose +24, notes 25,37,30,42)
pcm_c, sr_c, loop_c = load_aiff("sfx_9", "03")
tun_c = sr_c / float(OUT_SR)
dt_sfx = 1.0 / 60.0
coin_mix = np.zeros((int(0.95 * OUT_SR), 2), dtype=np.float32)
t_cur = 0.0
for semi, ticks, vel in [(49, 2, 55), (61, 7, 115), (54, 5, 55), (66, 55, 120)]:
    s0 = int(t_cur * OUT_SR)
    step = (2.0 ** ((semi - 39.0) / 12.0)) * tun_c
    w = synth_note(pcm_c, loop_c, step, int(ticks * dt_sfx * OUT_SR), int(0.08 * OUT_SR), vel / 127.0, vel / 127.0)
    end = min(len(coin_mix), s0 + len(w))
    coin_mix[s0:end] += w[:end - s0]
    t_cur += ticks * dt_sfx
save_mp3(coin_mix, os.path.join(OUT_DIR, "coin.mp3"))

# 4. Authentic Wooden Castle Door Open SFX (.sound_general_open_wood_door: sfx_5/01 + sfx_5/02)
door_mix = np.zeros((int(1.65 * OUT_SR), 2), dtype=np.float32)
t_cur = 0.0
for sname, ticks, vel in [("01", 24, 115), ("02", 72, 90)]:
    pcm_d, sr_d, loop_d = load_aiff("sfx_5", sname)
    s0 = int(t_cur * OUT_SR)
    w = synth_note(pcm_d, loop_d, sr_d / float(OUT_SR), int(ticks * dt_sfx * OUT_SR), int(0.1 * OUT_SR), vel / 127.0, vel / 127.0)
    end = min(len(door_mix), s0 + len(w))
    door_mix[s0:end] += w[:end - s0]
    t_cur += ticks * dt_sfx
save_mp3(door_mix, os.path.join(OUT_DIR, "door_open.mp3"))

# 5. Extra Mario voices from sfx_mario_peach (01 = Hoohoo!, 09 = Yah!)
for sname, out_f in [("01", "mario_hoohoo.mp3"), ("09", "mario_yah.mp3")]:
    in_aiff = os.path.join(R96_SOUND, "samples", "sfx_mario_peach", f"{sname}.aiff")
    if os.path.exists(in_aiff):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", in_aiff, "-b:a", "128k", os.path.join(OUT_DIR, out_f)], check=True)
        print(f"Converted {out_f}")
