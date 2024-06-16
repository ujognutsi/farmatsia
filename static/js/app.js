function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const init = () => {
    const cards = document.querySelectorAll('.card')

    for (const card of cards) {
        
        const likeButton = card.querySelector('.like-button')
        const dislikeButton = card.querySelector('.dislike-button')
        const likeCounter = card.querySelector('.like-counter')
        const dislikeCounter = card.querySelector('.dislike-counter')
        const questionId = card.dataset.questionid
        likeButton.addEventListener('click', () => {
            alert("jeje")
            const request = new Request(`${questionId}/questionlike`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    key: 'value',
                    anotherKey: 'anotherValue'
                })
            })

            fetch(request)
                .then((response) => response.json())
                .then((data) => likeCounter.innerHTML = data.likes_count)
        })

        dislikeButton.addEventListener('click', () => {
            const request = new Request(`${questionId}/questiondislike`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    key: 'value',
                    anotherKey: 'anotherValue'
                })
            })

            fetch(request)
                .then((response) => response.json())
                .then((data) => dislikeCounter.innerHTML = data.dislikes_count)
        })
    }
}

init()