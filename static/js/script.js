document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search-input");
  const resultsDiv = document.getElementById("autocomplete-results");

  searchInput.addEventListener("input", () => {
    const term = searchInput.value.trim();
    if (term.length < 1) {
      resultsDiv.innerHTML = "";
      return;
    }

    fetch(`/autocomplete?term=${encodeURIComponent(term)}`)
      .then(res => res.json())
      .then(data => {
        resultsDiv.innerHTML = "";
        data.results.forEach(item => {
          const div = document.createElement("div");
          div.textContent = item;
          div.style.padding = "5px";
          div.style.cursor = "pointer";

          div.addEventListener("click", () => {
            searchInput.value = item;
            resultsDiv.innerHTML = "";
          });

          resultsDiv.appendChild(div);
        });
      }).catch(err => console.error("Autocomplete error:", err));
  });

  document.addEventListener("click", (e) => {
    if (!resultsDiv.contains(e.target) && e.target !== searchInput) {
      resultsDiv.innerHTML = "";
    }
  });
});

function handleImageError(imgElement, gameId) {
  imgElement.onerror = null; 


  fetch(`/api/game-image-fallback/${gameId}`)
    .then(response => response.json())
    .then(data => {
      if (data.image_url) {
        imgElement.src = data.image_url;
      } else {
        imgElement.src = 'https://img.freepik.com/free-vector/illustration-gallery-icon_53876-27002.jpg';
      }
    })
    .catch(() => {
      imgElement.src = 'https://img.freepik.com/free-vector/illustration-gallery-icon_53876-27002.jpg';
    });
  
}




const toggleBtn = document.querySelector('.theme-toggle');


window.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.body.setAttribute('data-theme', 'dark');
  } else {
    document.body.removeAttribute('data-theme');
  }
});


toggleBtn.addEventListener('click', () => {
  if (document.body.getAttribute('data-theme') === 'dark') {
    document.body.removeAttribute('data-theme');
    localStorage.setItem('theme', 'light');
  } else {
    document.body.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  }
});

