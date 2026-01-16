const params = new URLSearchParams(window.location.search);
const surahId = parseInt(params.get('id'));
const selectedReciterId = params.get('reciter') || localStorage.getItem('selectedReciter') || 'bader-hafs';

const audio = document.getElementById('surah-audio');
const themeSelect = document.getElementById('themeSelect');
const riwayaSelect = document.getElementById('riwayaSelect');

let allReciters = [];
let currentReciter = null;
let currentSurah = null;

// تحميل الثيم المختار
const savedTheme = localStorage.getItem('theme') || 'light';
document.body.classList.add(`theme-${savedTheme}`);
themeSelect.value = savedTheme;

// وظيفة تحديث مصدر الصوت
function updateAudioSource() {
  if (!currentReciter || !currentSurah) return;
  
  // التحقق مما إذا كانت السورة محملة أوفلاين
  if (window.python && window.python.is_downloaded(currentSurah.id)) {
      audio.src = window.python.get_local_path(currentSurah.id);
      console.log("تعمل الآن من الذاكرة المحلية");
  } else {
      const paddedId = String(currentSurah.id).padStart(3, '0');
      audio.src = `${currentReciter.baseURL}${paddedId}.mp3`;
      console.log("تعمل الآن عبر الإنترنت");
  }
}

// وظيفة التحميل
function downloadCurrentSurah() {
    if (!currentSurah) return;
    alert("بدأ التحميل، يرجى الانتظار...");
    const paddedId = String(currentSurah.id).padStart(3, '0');
    const url = `${currentReciter.baseURL}${paddedId}.mp3`;
    
    if (window.python) {
        const result = window.python.download_audio(url, currentSurah.id);
        if (result !== "error") {
            alert("تم التحميل بنجاح!");
            updateAudioSource();
        } else {
            alert("فشل التحميل.");
        }
    }
}

// جلب البيانات الأساسية
fetch('reciters.json')
  .then(res => res.json())
  .then(data => {
    allReciters = data.reciters;
    currentReciter = allReciters.find(r => r.id === selectedReciterId);
    return fetch('data.json');
  })
  .then(res => res.json())
  .then(data => {
    currentSurah = data.surahs.find(s => s.id === surahId);
    updateAudioSource();
  });