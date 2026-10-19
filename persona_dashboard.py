"""
Studi Kasus: Dashboard Berbasis User Persona + Audit Kontras WCAG
Berdasarkan kuliah umum "Human-Computer Interaction & Data Visualization" (Dr. Arafat Febriandirza, BRIN).

Satu dataset (penjualan toko, SINTETIS) disajikan dalam tiga tampilan untuk tiga persona berbeda.
Python menghasilkan data, memeriksa rasio kontras palet warna (WCAG 2.x), lalu membangun docs/index.html.
Tanpa dependensi eksternal. Persona bersifat ASUMSI (belum dari riset pengguna).
"""
import csv
import json
import math
import random
from pathlib import Path

DOCS = Path("docs")
rnd = random.Random(2026)
CATS = {"Minuman": 420, "Makanan": 360, "Camilan": 180, "Peralatan": 120}   # basis penjualan (juta Rp/bulan)
TREN = {"Minuman": .015, "Makanan": .005, "Camilan": -.012, "Peralatan": 0.0}
REGS = {"Utara": 1.1, "Tengah": 1.0, "Selatan": .85}


def buat_data():
    rows = []
    for m in range(12):                                   # 0 = Okt 2025 ... 11 = Sep 2026
        musim = 1 + .12 * math.sin(2 * math.pi * (m + 1) / 12)
        for c, base in CATS.items():
            for r, w in REGS.items():
                tren = TREN[c] * (2.2 if (c == "Camilan" and r == "Selatan") else 1)   # Camilan-Selatan paling turun
                v = base * w / 3 * musim * (1 + tren) ** m * (1 + rnd.uniform(-.05, .05))
                t = base * w / 3 * musim * 1.02
                rows.append({"m": m, "c": c, "r": r, "v": round(v, 1), "t": round(t, 1)})
    return rows


# ---------- audit kontras WCAG ----------
def lum(h):
    ch = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(ch[0]) + .7152 * f(ch[1]) + .0722 * f(ch[2])


def rasio(a, b):
    hi, lo = sorted([lum(a), lum(b)], reverse=True)
    return (hi + .05) / (lo + .05)


def nilai(r, teks=True):
    if teks:
        return "AAA" if r >= 7 else "AA" if r >= 4.5 else "Gagal"
    return "Lolos (≥3:1)" if r >= 3 else "Gagal (<3:1)"


def audit():
    teks = [("Teks hitam di latar krem", "#111111", "#fffbee"), ("Teks hitam di latar putih", "#111111", "#ffffff"),
            ("Teks hitam di kuning", "#111111", "#ffd23f"), ("Teks hitam di pink", "#111111", "#ff9ecd"),
            ("Teks hitam di hijau", "#111111", "#7ee8a2"), ("Teks hitam di biru", "#111111", "#7cc4ff"),
            ("Teks hitam di merah", "#111111", "#ff6b6b"), ("Teks putih di hitam", "#ffffff", "#111111"),
            ("Teks abu #666 di putih", "#666666", "#ffffff")]
    grafis = [("Isi batang kuning vs putih", "#ffd23f", "#ffffff"), ("Isi batang biru vs putih", "#7cc4ff", "#ffffff"),
              ("Garis tepi hitam vs putih", "#111111", "#ffffff")]
    out = [{"n": n, "r": round(rasio(a, b), 2), "h": nilai(rasio(a, b)), "t": "teks", "fg": a, "bg": b} for n, a, b in teks]
    out += [{"n": n, "r": round(rasio(a, b), 2), "h": nilai(rasio(a, b), False), "t": "grafis", "fg": a, "bg": b} for n, a, b in grafis]
    return out


def main():
    data = buat_data()
    kontras = audit()
    print("Audit kontras WCAG:")
    for k in kontras:
        print(f"  {k['n']:32} {k['r']:>5}:1  {k['h']}")
    DOCS.mkdir(exist_ok=True)
    (DOCS / ".nojekyll").touch()
    with open(DOCS / "data_penjualan.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["m", "c", "r", "v", "t"])
        w.writeheader(); w.writerows(data)
    html = TEMPLATE.replace("__DATA__", json.dumps(data, separators=(",", ":"))).replace("__META__", json.dumps({"kontras": kontras}))
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    print(f"Selesai: {len(data)} baris data -> docs/index.html")


TEMPLATE = r'''<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Satu Data, Tiga Pengguna</title>
<style>
:root{--ink:#111;--bg:#fffbee;--y:#ffd23f;--p:#ff9ecd;--g:#7ee8a2;--b:#7cc4ff;--r:#ff6b6b}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Space Grotesk","Helvetica Neue",Arial,sans-serif;line-height:1.5}
.wrap{max-width:1260px;margin:auto;padding:28px 22px 44px}
h1{margin:0;font-size:clamp(2rem,6vw,3.5rem);font-weight:800;letter-spacing:-.03em;line-height:1.05}
h1 mark{background:var(--y);padding:0 .15em;border:3px solid var(--ink);box-shadow:5px 5px 0 var(--ink);display:inline-block;transform:rotate(-1.5deg)}
.sub{margin:14px 0 20px;font-weight:600;max-width:800px}
.bar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;background:#fff;border:3px solid var(--ink);box-shadow:8px 8px 0 var(--ink);padding:12px 14px;margin-bottom:26px}
.bar b{font-size:.8rem;text-transform:uppercase}
button{font:inherit;font-weight:800;color:var(--ink);border:3px solid var(--ink);background:#fff;padding:7px 16px;cursor:pointer;box-shadow:3px 3px 0 var(--ink);transition:.1s}
button:hover{transform:translate(-2px,-2px)}button:focus-visible{outline:4px solid var(--b);outline-offset:2px}
button.on{background:var(--y);transform:translate(2px,2px);box-shadow:1px 1px 0 var(--ink)}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:22px;align-items:start}.s4{grid-column:span 4}.s8{grid-column:span 8}.s5{grid-column:span 5}.s7{grid-column:span 7}.s12{grid-column:span 12}
.card{background:#fff;border:3px solid var(--ink);box-shadow:7px 7px 0 var(--ink);padding:16px 18px}.card h2{margin:0 0 10px;font-size:1rem;text-transform:uppercase}.card h3{margin:12px 0 4px;font-size:.82rem;text-transform:uppercase}
.card p,.card li{font-size:.9rem;font-weight:500}.card ul{margin:0;padding-left:18px}
.kp{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:14px}.kp div{border:3px solid var(--ink);box-shadow:4px 4px 0 var(--ink);padding:8px 10px}
.kp span{display:block;font-size:.7rem;font-weight:700;text-transform:uppercase}.kp b{font-size:1.5rem}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 12px;align-items:center}.chips small{font-weight:800;text-transform:uppercase;font-size:.72rem}.chips button{padding:4px 12px;box-shadow:2px 2px 0 var(--ink)}
table{border-collapse:collapse;width:100%;font-size:.84rem;border:3px solid var(--ink)}th{background:var(--ink);color:#fff;padding:7px;font-size:.7rem;text-transform:uppercase;text-align:left}td{padding:7px;border-top:2px solid var(--ink);font-weight:600}
.badge{display:inline-block;border:2px solid var(--ink);padding:1px 8px;font-weight:800;font-size:.78rem}
.alert{border:3px solid var(--ink);padding:8px 12px;margin:8px 0;font-weight:700;font-size:.88rem;display:flex;gap:10px;align-items:center}
.pr{display:grid;gap:10px}.pr div{border:3px solid var(--ink);padding:8px 10px;font-size:.86rem;font-weight:500}.pr b{display:block;text-transform:uppercase;font-size:.74rem}
.note{margin:14px 0 0;border:3px solid var(--ink);background:var(--r);padding:8px 12px;font-weight:700;font-size:.85rem}
.big{font-size:1.35rem;line-height:1.6}.big .kp b{font-size:2.2rem}.big button{font-size:1.2rem;padding:12px 22px}.big p{font-size:1.25rem;font-weight:600}
.pass{background:var(--g)}.fail{background:var(--r)}
@media(max-width:900px){.s4,.s8,.s5,.s7{grid-column:span 12}}
</style></head><body><div class="wrap">
<h1>Satu Data, <mark>Tiga</mark> Pengguna</h1>
<p class="sub">Data penjualan yang sama, disajikan berbeda untuk tiga persona. Pilih persona di bawah dan perhatikan bagaimana kebutuhan pengguna membentuk keputusan desain. Studi kasus kuliah umum HCI &amp; Data Visualization (Dr. Arafat Febriandirza, BRIN).</p>
<div class="bar"><b>Persona</b><button id="t-analis" onclick="setP('analis')">Analis Data</button><button id="t-manajer" onclick="setP('manajer')">Manajer</button><button id="t-lansia" onclick="setP('lansia')">Pengguna Tua</button><span style="font-weight:700;font-size:.85rem">Data sintetis · persona berdasarkan asumsi</span></div>
<div class="grid">
<div class="card s4" id="persona"></div>
<div class="card s8" id="view"></div>
<div class="card s7" id="why"></div>
<div class="card s5"><h2>Audit kontras warna (WCAG)</h2><div id="audit"></div>
<p style="font-size:.8rem">Teks normal: AA ≥ 4,5:1, AAA ≥ 7:1. Objek grafis: ≥ 3:1. Isi batang berwarna terang gagal 3:1 terhadap putih, karena itu setiap batang diberi <b>garis tepi hitam</b> dan <b>label langsung</b>, sehingga informasi tidak hanya bergantung pada warna.</p></div>
<div class="card s12"><h2>Catatan</h2><ul><li>Semua sumbu grafik dimulai dari nol agar tidak menyesatkan (prinsip etika desain visualisasi).</li><li>Persona di sini adalah <b>asumsi awal</b>. Menurut materi, persona yang baik disusun dari riset empiris (wawancara, survei, observasi), jadi perlu divalidasi dengan pengguna sungguhan.</li><li>Audit otomatis hanya mengecek kontras warna, bukan seluruh aspek aksesibilitas. Pengujian dengan pengguna dan pembaca layar tetap diperlukan.</li></ul></div>
</div></div>
<script>
const D=__DATA__,M=__META__,$=i=>document.getElementById(i);
const ML=['Okt','Nov','Des','Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep'],CATS=['Minuman','Makanan','Camilan','Peralatan'],REGS=['Utara','Tengah','Selatan'];
const COL={Minuman:'#7cc4ff',Makanan:'#7ee8a2',Camilan:'#ffd23f',Peralatan:'#ff9ecd'},DASH={Minuman:'',Makanan:'8 4',Camilan:'2 4',Peralatan:'10 3 2 3'};
const fmt=v=>Math.round(v).toLocaleString('id-ID'),sum=a=>a.reduce((x,y)=>x+y,0),pc=(a,b)=>b?(a/b-1)*100:0;
const sgn=v=>(v>=0?'+':'')+v.toFixed(1)+'%';
function ser(f){const s=Array(12).fill(0),t=Array(12).fill(0);D.filter(f).forEach(r=>{s[r.m]+=r.v;t[r.m]+=r.t});return{s,t}}
function lineSvg(lines,fs){fs=fs||11;const w=680,h=270,p={l:50,r:96,t:14,b:30},mx=Math.max(1,...lines.flatMap(l=>l.v))*1.1;
 const X=i=>p.l+i*(w-p.l-p.r)/11,Y=v=>h-p.b-v/mx*(h-p.t-p.b);
 let s=`<svg viewBox="0 0 ${w} ${h}" width="100%" role="img" aria-label="Grafik garis penjualan per bulan, sumbu dimulai dari nol">`;
 for(let k=0;k<=4;k++){const v=mx*k/4;s+=`<line x1="${p.l}" x2="${w-p.r}" y1="${Y(v)}" y2="${Y(v)}" stroke="#ccc"/><text x="${p.l-6}" y="${Y(v)+4}" text-anchor="end" font-size="${fs}">${fmt(v)}</text>`}
 ML.forEach((m,i)=>s+=`<text x="${X(i)}" y="${h-9}" text-anchor="middle" font-size="${fs}">${m}</text>`);
 lines.forEach(l=>{s+=`<polyline fill="none" stroke="#111" stroke-width="3" ${l.d?`stroke-dasharray="${l.d}"`:''} points="${l.v.map((v,i)=>X(i)+','+Y(v)).join(' ')}"/>`;
  l.v.forEach((v,i)=>s+=`<circle cx="${X(i)}" cy="${Y(v)}" r="4.5" fill="${l.c}" stroke="#111" stroke-width="2"><title>${l.n} ${ML[i]}: Rp ${fmt(v)} jt</title></circle>`);
  s+=`<text x="${X(11)+8}" y="${Y(l.v[11])+4}" font-size="${fs+1}" font-weight="800">${l.n}</text>`});
 return s+'</svg>'}
function barSvg(items,fs){fs=fs||13;const w=680,rh=fs*3.2,h=items.length*rh+10,mx=Math.max(1,...items.map(i=>i.v)),L=fs*8.5;
 return `<svg viewBox="0 0 ${w} ${h}" width="100%" role="img" aria-label="Grafik batang, sumbu dimulai dari nol">`+items.map((it,i)=>{const bw=it.v/mx*(w-L-110);
 return `<text x="0" y="${i*rh+rh/1.7}" font-size="${fs}" font-weight="800">${it.l}</text><rect x="${L}" y="${i*rh+4}" width="${bw}" height="${rh-12}" fill="${it.c}" stroke="#111" stroke-width="3"><title>${it.l}: Rp ${fmt(it.v)} jt</title></rect><text x="${L+bw+8}" y="${i*rh+rh/1.7}" font-size="${fs}" font-weight="800">${fmt(it.v)}</text>`}).join('')+'</svg>'}
const P={
analis:{nama:'Dimas, 27 tahun',peran:'Analis Data',tujuan:['Mengeksplorasi pola per kategori dan wilayah','Membandingkan beberapa seri sekaligus','Menemukan penyebab perubahan angka'],kendala:['Ringkasan terlalu agregat, tidak bisa dibedah','Tidak ada filter yang fleksibel'],skenario:'Dimas curiga ada kategori yang melemah. Ia menyaring kategori dan wilayah, membandingkan tren, lalu membaca tabel angkanya.',
 why:[['Visibility','Semua filter terlihat sekaligus; kondisi aktif ditandai warna kuning.'],['Feedback','Grafik, kartu, dan tabel berubah seketika saat filter diklik (real-time).'],['Affordance','Chip berbentuk tombol dengan bayangan, jelas dapat diklik.'],['Gestalt: proximity','Label seri diletakkan di ujung garisnya, bukan di legenda terpisah.'],['Preattentive','Garis dibedakan pola dan penanda, bukan hanya warna.']]},
manajer:{nama:'Bu Ratna, 45 tahun',peran:'Manajer Operasional',tujuan:['Mengetahui kondisi bisnis dalam hitungan detik','Menemukan hal yang perlu ditindak','Mengomunikasikan ke direksi'],kendala:['Terlalu banyak grafik dan kontrol','Waktu terbatas antar rapat'],skenario:'Sebelum rapat, Bu Ratna membuka dashboard 30 detik: apakah target tercapai, dan apa yang perlu perhatian?',
 why:[['Constraints','Hanya satu kontrol (periode) agar tidak salah atau bingung memilih.'],['Visibility','Tiga angka kunci di atas; peringatan berada di tempat yang terlihat.'],['Preattentive','Merah/kuning dan ukuran besar langsung menarik mata ke yang bermasalah.'],['Beban kognitif','Satu grafik saja (total vs target) untuk meminimalkan extraneous load.'],['Consistency','Warna merah selalu berarti perlu tindakan.']]},
lansia:{nama:'Pak Hasan, 64 tahun',peran:'Pemilik usaha, penglihatan menurun',tujuan:['Melihat kategori yang paling laku','Membaca angka tanpa memicingkan mata','Tidak tersesat di antarmuka'],kendala:['Teks kecil sulit dibaca','Banyak elemen membuatnya bingung','Kurang akrab dengan istilah teknis'],skenario:'Pak Hasan ingin tahu produk apa yang paling laku bulan ini, dalam bahasa biasa dan huruf besar.',
 why:[['WCAG: Perceivable','Teks besar, kontras hitam di putih, dan label langsung pada batang.'],['WCAG: Operable','Hanya dua tombol besar dengan area klik luas.'],['WCAG: Understandable','Ringkasan ditulis dalam kalimat biasa, bukan istilah teknis.'],['Constraints','Satu grafik dan satu pertanyaan per layar.'],['Feedback','Tombol terpilih berubah warna dan kalimat ringkasan langsung diperbarui.']]}};
let cur='analis',fc=new Set(CATS),fr=new Set(REGS),np=3,nl=1;
function setP(p){cur=p;render()}
function tog(set,v){set.has(v)?set.delete(v):set.add(v);if(!set.size)CATS.concat(REGS).forEach(x=>set.add(x));render()}
function chips(label,all,set,name){return `<div class="chips"><small>${label}</small>${all.map(x=>`<button class="${set.has(x)?'on':''}" aria-pressed="${set.has(x)}" onclick="tog(${name},'${x}')">${x}</button>`).join('')}</div>`}
function vAnalis(){const f=r=>fc.has(r.c)&&fr.has(r.r),a=ser(f),L=CATS.filter(c=>fc.has(c)).map(c=>({n:c,c:COL[c],d:DASH[c],v:ser(r=>r.c===c&&fr.has(r.r)).s}));
 const l3=sum(a.s.slice(9)),p3=sum(a.s.slice(6,9)),t3=sum(a.t.slice(9));
 const rows=CATS.filter(c=>fc.has(c)).map(c=>{const s=ser(r=>r.c===c&&fr.has(r.r));return{c,tot:sum(s.s),g:pc(sum(s.s.slice(9)),sum(s.s.slice(6,9))),a:sum(s.s.slice(9))/sum(s.t.slice(9))*100}}).sort((x,y)=>y.tot-x.tot);
 return `<h2>Eksplorasi (Analis Data)</h2>${chips('Kategori',CATS,fc,'fc')}${chips('Wilayah',REGS,fr,'fr')}
 <div class="kp"><div style="background:var(--b)"><span>Total 12 bln (jt)</span><b>${fmt(sum(a.s))}</b></div><div style="background:var(--g)"><span>3 bln vs 3 sebelumnya</span><b>${sgn(pc(l3,p3))}</b></div><div style="background:var(--y)"><span>Capaian target 3 bln</span><b>${(l3/t3*100).toFixed(0)}%</b></div></div>
 ${lineSvg(L)}<h3>Rincian per kategori</h3><table><tr><th>Kategori</th><th>Total (jt)</th><th>Perubahan 3 bln</th><th>Capaian target</th></tr>${rows.map(r=>`<tr><td>${r.c}</td><td>${fmt(r.tot)}</td><td><span class="badge" style="background:${r.g<0?'var(--r)':'var(--g)'}">${sgn(r.g)}</span></td><td>${r.a.toFixed(0)}%</td></tr>`).join('')}</table>`}
function vManajer(){const a=ser(()=>true),n=np,l=sum(a.s.slice(12-n)),t=sum(a.t.slice(12-n)),pv=n<=6?sum(a.s.slice(12-2*n,12-n)):null;
 const bad=[];CATS.forEach(c=>REGS.forEach(r=>{const s=ser(x=>x.c===c&&x.r===r),v=sum(s.s.slice(12-n)),tt=sum(s.t.slice(12-n));bad.push({c,r,p:v/tt*100})}));
 const al=bad.filter(b=>b.p<97).sort((x,y)=>x.p-y.p).slice(0,3);
 return `<h2>Ringkasan (Manajer)</h2><div class="chips"><small>Periode</small>${[3,6,12].map(x=>`<button class="${n===x?'on':''}" aria-pressed="${n===x}" onclick="np=${x};render()">${x} bulan</button>`).join('')}</div>
 <div class="kp"><div style="background:var(--b)"><span>Penjualan (jt)</span><b>${fmt(l)}</b></div><div style="background:${l>=t?'var(--g)':'var(--r)'}"><span>Capaian target</span><b>${(l/t*100).toFixed(0)}%</b></div><div style="background:var(--y)"><span>Vs periode sebelumnya</span><b>${pv?sgn(pc(l,pv)):'-'}</b></div></div>
 ${lineSvg([{n:'Aktual',c:'#7cc4ff',d:'',v:a.s},{n:'Target',c:'#fff',d:'6 5',v:a.t}])}
 <h3>Perlu perhatian</h3>${al.length?al.map(b=>`<div class="alert" style="background:${b.p<90?'var(--r)':'var(--y)'}"><span class="badge" style="background:#fff">${b.p.toFixed(0)}%</span>${b.c} di wilayah ${b.r} di bawah target</div>`).join(''):'<div class="alert" style="background:var(--g)">Semua kategori mendekati atau di atas target.</div>'}`}
function vLansia(){const n=nl,items=CATS.map(c=>({l:c,c:COL[c],v:sum(ser(r=>r.c===c).s.slice(12-n))})).sort((x,y)=>y.v-x.v);
 const tot=sum(items.map(i=>i.v)),prev=sum(ser(()=>true).s.slice(12-2*n,12-n)),top=items[0];
 return `<div class="big"><h2>Penjualan (Pengguna Tua)</h2><div class="chips"><button class="${n===1?'on':''}" aria-pressed="${n===1}" onclick="nl=1;render()">Bulan ini</button><button class="${n===3?'on':''}" aria-pressed="${n===3}" onclick="nl=3;render()">3 bulan terakhir</button></div>
 <p>Yang paling laku: <b>${top.l}</b>, sekitar Rp ${fmt(top.v)} juta. Total semua barang Rp ${fmt(tot)} juta, ${tot>=prev?'naik':'turun'} ${Math.abs(pc(tot,prev)).toFixed(0)}% dibanding sebelumnya.</p>${barSvg(items,17)}</div>`}
function render(){
 ['analis','manajer','lansia'].forEach(k=>{const b=$('t-'+k);b.className=k===cur?'on':''});
 const p=P[cur];
 $('persona').innerHTML=`<h2>Persona</h2><p><b>${p.nama}</b><br>${p.peran}</p><h3>Tujuan</h3><ul>${p.tujuan.map(x=>`<li>${x}</li>`).join('')}</ul><h3>Kendala</h3><ul>${p.kendala.map(x=>`<li>${x}</li>`).join('')}</ul><h3>Skenario</h3><p>${p.skenario}</p>`;
 $('view').innerHTML={analis:vAnalis,manajer:vManajer,lansia:vLansia}[cur]();
 const cl=['var(--b)','var(--g)','var(--p)','var(--y)','var(--b)'];
 $('why').innerHTML=`<h2>Kenapa tampilan ini dirancang begini?</h2><div class="pr">${p.why.map((w,i)=>`<div style="background:${cl[i]}"><b>${w[0]}</b>${w[1]}</div>`).join('')}</div>`;
 $('audit').innerHTML='<table><tr><th>Pasangan warna</th><th>Rasio</th><th>Hasil</th></tr>'+M.kontras.map(k=>`<tr><td>${k.n}</td><td>${k.r}:1</td><td><span class="badge ${k.h.startsWith('Gagal')?'fail':'pass'}">${k.h}</span></td></tr>`).join('')+'</table>';
}
render();
</script></body></html>'''

if __name__ == "__main__":
    main()
