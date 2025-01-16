document.getElementById('bookForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const query = document.getElementById('bookQuery').value;

    if (query.trim() === "") {
        alert("Please enter a book title!");
        return;
    }

    fetch(`/search_book?q=${query}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {

                const recommendationsContainer = document.getElementById('recommendations');
                recommendationsContainer.innerHTML = `
                  <h2>Recommended Songs</h2>
              `;

                data.recommended_songs.forEach((song, index) => {
                    const songElement = document.createElement('p');
                    songElement.innerHTML = `<strong>${index + 1}. </strong><a href="${song.song_url}" target="_blank">${song.song_name}</a>`;
                    recommendationsContainer.appendChild(songElement);
                });
                recommendationsContainer.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("There was an error processing your request.");
        });
});