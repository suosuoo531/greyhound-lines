const destinations = [
    'New York City', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
    'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
    'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte',
    'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington D.C.',
    'Boston', 'Nashville', 'Baltimore', 'Oklahoma City', 'Louisville',
    'Portland', 'Las Vegas', 'Memphis', 'Detroit', 'Milwaukee'
];

const cityIcons = {
    'New York City': '🗽',
    'Los Angeles': '🏖️',
    'Chicago': '🌆',
    'Houston': '🚀',
    'Phoenix': '🌵',
    'Philadelphia': '🔔',
    'San Antonio': '💃',
    'San Diego': '🏄',
    'Dallas': '🤠',
    'San Jose': '💻',
    'Austin': '🎵',
    'Jacksonville': '🌊',
    'Fort Worth': '🐎',
    'Columbus': '🏛️',
    'Charlotte': '🏦',
    'San Francisco': '🌉',
    'Indianapolis': '🏎️',
    'Seattle': '☔',
    'Denver': '🏔️',
    'Washington D.C.': '🏛️',
    'Boston': '🎓',
    'Nashville': '🎸',
    'Baltimore': '⚓',
    'Oklahoma City': '🏜️',
    'Louisville': '🏇',
    'Portland': '🌹',
    'Las Vegas': '🎰',
    'Memphis': '🎷',
    'Detroit': '🚗',
    'Milwaukee': '🍺'
};

let isLoading = false;

function getRandomItem(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function getCityIcon(city) {
    return cityIcons[city] || '🌆';
}

function initDestinationsGrid() {
    const grid = document.getElementById('destinationsGrid');
    destinations.slice(0, 15).forEach(city => {
        const card = document.createElement('div');
        card.className = 'destination-card';
        card.innerHTML = `
            <span class="city-icon">${getCityIcon(city)}</span>
            <span class="city-name">${city}</span>
        `;
        card.onclick = () => selectDestination(city);
        grid.appendChild(card);
    });
}

function showGoogleMap(location) {
    const iframe = document.getElementById('googleMap');
    const placeholder = document.getElementById('mapPlaceholder');
    const encodedLocation = encodeURIComponent(location + ', USA');
    iframe.src = `https://www.google.com/maps/embed/v1/place?key=AIzaSyA-aWwZ5xP5f8k4v9z8x7v6b5n4m3l2k1j&q=${encodedLocation}`;
    iframe.style.display = 'block';
    placeholder.style.display = 'none';
}

function showYouTubeVideo(videoId) {
    const container = document.getElementById('videoPlayerContainer');
    const iframe = document.getElementById('videoPlayer');
    iframe.src = `https://www.youtube.com/embed/${videoId}`;
    container.style.display = 'block';
}

function showLoading(loading) {
    isLoading = loading;
    const contentTitle = document.getElementById('contentTitle');
    const contentDate = document.getElementById('contentDate');
    
    if (loading) {
        contentTitle.textContent = '⏳ 正在生成内容...';
        contentDate.textContent = '请稍候，这可能需要几分钟...';
    }
}

function showError(message) {
    const contentTitle = document.getElementById('contentTitle');
    const contentDate = document.getElementById('contentDate');
    const videoInfo = document.getElementById('videoInfo');
    const englishContent = document.getElementById('englishContent');
    const chineseContent = document.getElementById('chineseContent');
    const videoPlayerContainer = document.getElementById('videoPlayerContainer');
    
    contentTitle.textContent = '❌ 出错了';
    contentDate.textContent = message;
    videoInfo.innerHTML = '<p>请稍后重试或选择另一个城市</p>';
    englishContent.innerHTML = '<p class="placeholder-text">暂无内容</p>';
    chineseContent.innerHTML = '<p class="placeholder-text">暂无内容</p>';
    videoPlayerContainer.style.display = 'none';
}

async function selectDestination(city) {
    if (isLoading) return;
    
    document.getElementById('toCity').textContent = city;
    animateBus();
    showGoogleMap(city);
    await generateContent(city);
}

function animateBus() {
    const bus = document.getElementById('busMoving');
    const parent = bus.parentElement;
    bus.style.animation = 'none';
    setTimeout(() => {
        bus.style.animation = 'moveBus 3s ease-in-out infinite';
    }, 10);
}

async function startJourney() {
    if (isLoading) return;
    
    const fromCity = getRandomItem(destinations);
    const toCity = getRandomItem(destinations.filter(c => c !== fromCity));
    
    document.getElementById('fromCity').textContent = fromCity;
    document.getElementById('toCity').textContent = toCity;
    
    animateBus();
    showGoogleMap(toCity);
    await generateContent(toCity);
}

async function generateContent(location) {
    showLoading(true);
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ location: location })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            displayContent(result);
        } else {
            showError(result.message || '生成内容失败');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('网络错误，请稍后重试');
    } finally {
        showLoading(false);
    }
}

function displayContent(data) {
    const now = new Date();
    const dateStr = now.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    document.getElementById('contentTitle').textContent = `探索 ${data.location}`;
    document.getElementById('contentDate').textContent = dateStr;
    
    const videoInfo = document.getElementById('videoInfo');
    const lengthMinutes = Math.round(data.video.length / 60);
    
    videoInfo.innerHTML = `
        <p><strong>🎬 视频标题:</strong> ${data.video.title}</p>
        <p><strong>🔗 链接:</strong> <a href="${data.video.url}" target="_blank">${data.video.url}</a></p>
        <p><strong>👤 作者:</strong> ${data.video.author}</p>
        <p><strong>⏱️ 时长:</strong> ${lengthMinutes}分钟</p>
        <p><strong>📝 类型:</strong> 当地介绍 / 城市漫步</p>
    `;
    
    const englishContent = document.getElementById('englishContent');
    const chineseContent = document.getElementById('chineseContent');
    
    if (data.content.english) {
        englishContent.innerHTML = `<p>${escapeHtml(data.content.english)}</p>`;
    } else {
        englishContent.innerHTML = '<p class="placeholder-text">英文内容生成中...</p>';
    }
    
    if (data.content.chinese) {
        chineseContent.innerHTML = `<p>${escapeHtml(data.content.chinese)}</p>`;
    } else {
        chineseContent.innerHTML = '<p class="placeholder-text">中文翻译生成中...</p>';
    }
    
    showYouTubeVideo(data.video.id);
    
    const contentCard = document.getElementById('contentCard');
    contentCard.classList.remove('animating');
    void contentCard.offsetWidth;
    contentCard.classList.add('animating');
    
    contentCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

document.addEventListener('DOMContentLoaded', () => {
    initDestinationsGrid();
});
