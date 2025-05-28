function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function answer_vote(answer_id, positive, rating) {
    alert("answer!");
    const formData = new FormData()
    formData.append('answer_id', answer_id)
    formData.append('positive', positive)

    const request = new Request('/answer/vote', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    });

    fetch(request)
        .then((response) => response.json())
        .then((data) => {
            if (data.error == 1) {
                alert(data.message);
            } else {
                rating.innerHTML = data.rating;
            }
        });
}

const answerItems = document.getElementsByClassName('answer-like-section');

for (let answerItem of answerItems) {
    const [, like, rating, dislike] = answerItem.children;
    like.addEventListener('click', (event) => answer_vote(like.dataset.id, true, rating), once=true);
    dislike.addEventListener('click', (event) => answer_vote(dislike.dataset.id, false, rating), once=true);
}


function question_vote(question_id, positive, rating) {
    const formData = new FormData()
    formData.append('question_id', question_id)
    formData.append('positive', positive)

    const request = new Request('/question/vote', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    });

    fetch(request)
        .then((response) => response.json())
        .then((data) => {
            if (data.error == 1) {
                alert(data.message);
            } else {
                rating.innerHTML = data.rating;
            }
        });
}

const questionItems = document.getElementsByClassName('question-like-section');

for (let questionItem of questionItems) {
    const [, like, rating, dislike] = questionItem.children;
    like.addEventListener('click', (event) => question_vote(like.dataset.id, true, rating), once=true);
    dislike.addEventListener('click', (event) => question_vote(dislike.dataset.id, false, rating), once=true);
}