"""
laptop_parser.py
================
Helper untuk parse deskripsi laptop dari CSV → specs terstruktur.
Tambahkan fungsi ini ke app.py atau import sebagai modul.
"""

import re


def parse_laptop_specs(nama: str, deskripsi: str) -> dict:
    """
    Parse deskripsi laptop dari CSV menjadi dict specs terstruktur.
    
    Args:
        nama     : nama_laptop dari CSV  (misal: "ASUS ROG Strix G16")
        deskripsi: deskripsi dari CSV    (misal: "Laptop gaming Intel i7 RAM 16GB RTX 4060 ...")
    
    Returns:
        dict dengan key:
            processor, gpu, ram, display,
            storage, kategori, tagline, deskripsi_panjang,
            tags (list), keunggulan (list of dict)
    """

    desc = deskripsi.lower()
    specs = {}

    # ── PROCESSOR ──────────────────────────────────────────────
    processor = "—"
    proc_patterns = [
        (r'intel\s+core\s+ultra\s+\d+',   lambda m: m.group().title()),
        (r'intel\s+core\s+i[3579][\s\-]\d+\w*', lambda m: m.group().title()),
        (r'intel\s+core\s+i[3579]',        lambda m: m.group().title()),
        (r'intel\s+i[3579]',               lambda m: m.group().replace('intel ', 'Intel Core ').title()),
        (r'ryzen\s+[3579](?:\s+\d+\w*)?', lambda m: 'AMD ' + m.group().title()),
        (r'amd\s+ryzen\s+[3579][\w\s]*',  lambda m: m.group().title()),
        (r'apple\s+m[123](?:\s+\w+)?',    lambda m: m.group().title()),
        (r'chip\s+m[123]',                 lambda m: m.group().replace('chip ', 'Apple ').title()),
        (r'intel\s+celeron',               lambda m: 'Intel Celeron'),
        (r'intel\s+core\s+ultra',          lambda m: 'Intel Core Ultra'),
        (r'intel\s+evo',                   lambda m: 'Intel Evo'),
        (r'amd\s+radeon',                  lambda m: 'AMD Ryzen'),   # fallback jika hanya radeon
    ]
    for pattern, formatter in proc_patterns:
        m = re.search(pattern, desc)
        if m:
            processor = formatter(m)
            break
    # Normalkan kapitalisasi: "Intel Core I7" → "Intel Core i7"
    processor = re.sub(r'\bI([3579])\b', r'i\1', processor)
    specs['processor'] = processor

    # ── GPU / GRAPHICS ─────────────────────────────────────────
    gpu = "Integrated"
    gpu_patterns = [
        r'rtx\s+40[0-9]{2}(?:\s+\d+gb)?',
        r'rtx\s+30[0-9]{2}(?:\s+\d+gb)?',
        r'rtx\s+20[0-9]{2}(?:\s+\d+gb)?',
        r'gtx\s+1[0-9]{3}(?:\s+\d+gb)?',
        r'radeon\s+rx\s+\w+',
        r'amd\s+radeon(?:\s+\w+)?',
    ]
    for pattern in gpu_patterns:
        m = re.search(pattern, desc)
        if m:
            gpu = m.group().upper().replace('  ', ' ')
            # Normalkan: "RTX 4060" bukan "RTX4060"
            gpu = re.sub(r'(RTX|GTX|RX)\s*(\d)', r'\1 \2', gpu)
            break
    specs['gpu'] = gpu

    # ── RAM ────────────────────────────────────────────────────
    ram = "8GB"
    m = re.search(r'ram\s+(\d+)\s*gb', desc)
    if m:
        ram = f"{m.group(1)}GB"
    else:
        # fallback: cari pola "16gb" tanpa kata "ram"
        m2 = re.search(r'\b(\d+)\s*gb\b', desc)
        if m2:
            ram = f"{m2.group(1)}GB"
    # Deteksi DDR type
    if 'ddr5' in desc:
        ram += ' DDR5'
    elif 'ddr4' in desc:
        ram += ' DDR4'
    specs['ram'] = ram

    # ── STORAGE ────────────────────────────────────────────────
    storage = "SSD"
    m = re.search(r'ssd\s+(\d+)\s*(tb|gb)', desc)
    if m:
        storage = f"SSD {m.group(1)}{m.group(2).upper()}"
    elif 'ssd' in desc:
        storage = "SSD"
    elif 'hdd' in desc:
        storage = "HDD"
    specs['storage'] = storage

    # ── DISPLAY ────────────────────────────────────────────────
    display = "FHD"
    display_parts = []
    if '4k' in desc:
        display_parts.append('4K')
    elif 'qhd' in desc or '2k' in desc:
        display_parts.append('QHD')
    elif 'fhd' in desc or '1080' in desc:
        display_parts.append('FHD')
    if 'oled' in desc:
        display_parts.append('OLED')
    m_hz = re.search(r'(\d+)\s*hz', desc)
    if m_hz:
        display_parts.append(f"{m_hz.group(1)}Hz")
    display = ' '.join(display_parts) if display_parts else 'FHD'
    specs['display'] = display

    # ── KATEGORI ───────────────────────────────────────────────
    tags = []
    if any(k in desc for k in ['gaming', 'rtx', 'gtx', 'radeon rx']):
        tags.append('Gaming')
    if any(k in desc for k in ['rtx 40', 'rtx 30']):
        tags.append('RTX Series')
    if 'ssd' in desc:
        tags.append('SSD Storage')
    if any(k in desc for k in ['content creation', 'creator', 'desain', 'render', 'editing']):
        tags.append('Creator')
    if any(k in desc for k in ['bisnis', 'kerja', 'kantor', 'office', 'thinkpad']):
        tags.append('Business')
    if any(k in desc for k in ['oled']):
        tags.append('OLED')
    if any(k in desc for k in ['tipis', 'ringan', 'slim', 'ultra']):
        tags.append('Slim')
    if any(k in desc for k in ['touchscreen', 'convertible', 'flip', 'yoga', 'flex']):
        tags.append('Touchscreen')
    if any(k in desc for k in ['mahasiswa', 'pelajar', 'kuliah', 'sekolah']):
        tags.append('Student')
    specs['tags'] = tags[:3]  # maks 3 tag

    # ── TAGLINE ────────────────────────────────────────────────
    # Buat tagline singkat dari deskripsi CSV (kalimat asli)
    specs['tagline'] = f'"{deskripsi}"'

    # ── DESKRIPSI PANJANG ──────────────────────────────────────
    # Generate deskripsi natural berdasarkan konten
    use_case = []
    if 'gaming' in desc:        use_case.append('gaming')
    if 'editing' in desc:       use_case.append('video editing')
    if 'desain' in desc:        use_case.append('desain grafis')
    if 'rendering' in desc or 'render' in desc: use_case.append('3D rendering')
    if 'mahasiswa' in desc or 'kuliah' in desc: use_case.append('kebutuhan perkuliahan')
    if 'bisnis' in desc or 'kerja' in desc:     use_case.append('produktivitas kerja')
    if 'office' in desc:        use_case.append('pekerjaan kantoran')
    if not use_case:             use_case.append('berbagai kebutuhan komputasi')

    use_str = ' dan '.join(use_case[:2])

    kelebihan = []
    if gpu != 'Integrated':     kelebihan.append(f'kartu grafis {gpu}')
    if 'oled' in desc:          kelebihan.append('layar OLED yang memukau')
    if 'tipis' in desc or 'slim' in desc: kelebihan.append('desain tipis dan ringan')
    if 'baterai' in desc:       kelebihan.append('baterai tahan lama')
    if 'touchscreen' in desc:   kelebihan.append('layar sentuh responsif')
    if not kelebihan:            kelebihan.append('performa handal')

    keleb_str = ', '.join(kelebihan[:2])

    specs['deskripsi_panjang'] = (
        f"Dirancang untuk {use_str}, {nama} hadir dengan {keleb_str}. "
        f"Dibekali prosesor {processor} dan RAM {ram}, laptop ini siap "
        f"menemani aktivitas harian Anda dengan performa yang optimal dan andal."
    )

    # ── KEUNGGULAN UTAMA ──────────────────────────────────────
    keunggulan = []

    if gpu != 'Integrated' and any(k in desc for k in ['rtx', 'gtx']):
        keunggulan.append({
            'icon': 'bi-gpu-card',
            'icon_color': 'purple',
            'judul': 'Performa Grafis Tinggi',
            'detail': f'Dilengkapi {gpu} untuk gaming dan rendering yang mulus tanpa hambatan.'
        })

    if 'oled' in desc:
        keunggulan.append({
            'icon': 'bi-display',
            'icon_color': 'blue',
            'judul': 'Layar OLED Memukau',
            'detail': 'Panel OLED menghadirkan warna akurat dan kontras tinggi untuk kreasi konten profesional.'
        })

    if 'tipis' in desc or 'ringan' in desc or 'slim' in desc:
        keunggulan.append({
            'icon': 'bi-feather',
            'icon_color': 'green',
            'judul': 'Desain Tipis & Ringan',
            'detail': 'Form factor ramping memudahkan mobilitas tanpa mengorbankan performa.'
        })

    if 'baterai' in desc:
        keunggulan.append({
            'icon': 'bi-battery-charging',
            'icon_color': 'yellow',
            'judul': 'Baterai Tahan Lama',
            'detail': 'Kapasitas baterai besar untuk menemani aktivitas seharian penuh tanpa khawatir kehabisan daya.'
        })

    if 'touchscreen' in desc or 'convertible' in desc:
        keunggulan.append({
            'icon': 'bi-hand-index-thumb',
            'icon_color': 'blue',
            'judul': 'Layar Sentuh Responsif',
            'detail': 'Mode touchscreen dan convertible memberikan fleksibilitas penggunaan yang lebih intuitif.'
        })

    if 'gaming' in desc and gpu != 'Integrated':
        keunggulan.append({
            'icon': 'bi-controller',
            'icon_color': 'purple',
            'judul': 'Siap untuk Gaming Serius',
            'detail': f'Kombinasi {processor} dan {gpu} menghadirkan frame rate tinggi di game AAA terkini.'
        })

    if any(k in desc for k in ['editing', 'creator', 'render']):
        keunggulan.append({
            'icon': 'bi-pencil-fill',
            'icon_color': 'yellow',
            'judul': 'Akurasi Warna Profesional',
            'detail': 'Layar tervalidasi untuk reproduksi warna presisi, ideal bagi kreator konten.'
        })

    if any(k in desc for k in ['bisnis', 'kerja', 'thinkpad']):
        keunggulan.append({
            'icon': 'bi-briefcase-fill',
            'icon_color': 'blue',
            'judul': 'Andalan Profesional',
            'detail': 'Dibangun untuk produktivitas maksimal dengan keyboard nyaman dan konektivitas lengkap.'
        })

    # Default fallback jika tidak ada keunggulan terdeteksi
    if not keunggulan:
        keunggulan = [
            {
                'icon': 'bi-lightning-fill',
                'icon_color': 'yellow',
                'judul': 'Performa Handal',
                'detail': f'Ditenagai {processor} untuk kelancaran multitasking sehari-hari.'
            },
            {
                'icon': 'bi-shield-check',
                'icon_color': 'purple',
                'judul': 'Kualitas Terjamin',
                'detail': 'Dibangun dengan material berkualitas tinggi untuk daya tahan jangka panjang.'
            }
        ]

    specs['keunggulan'] = keunggulan[:2]  # tampilkan maks 2

    return specs