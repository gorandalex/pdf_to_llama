token = localStorage.getItem("accessToken")

documents = document.getElementById("documents")

//const baseUrl = 'https://svitlogram.fly.dev';
const baseUrl = '';

const urlParams = new URLSearchParams(window.location.search);
const message = urlParams.get("message");

returnAnswer = document.getElementById("return_answer")

if (message) {
  returnAnswer.innerHTML = ""
  const returnAnswerDiv2 = document.createElement('div')
  returnAnswerDiv2.className = "modal-content rounded-4 shadow mb-2 mt-2"
  const returnAnswerDiv1 = document.createElement('div')
  returnAnswerDiv1.className = "col-md-12 py-2 align-items-centerv"
  const returnAnswerP = document.createElement('p')
  returnAnswerP.textContent = message;
  returnAnswerDiv1.appendChild(returnAnswerP)
  returnAnswerDiv2.appendChild(returnAnswerDiv1)
  returnAnswer.appendChild(returnAnswerDiv2)

}

const getUserById = async (user_id) => {
  const myHeaders = new Headers();
  myHeaders.append(
    "Authorization",
    `Bearer ${token}`);

  const requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
  };

  const response = await fetch(`${baseUrl}/api/users/users_id/${user_id}`, requestOptions)
  if (response.status === 200) {
    result = await response.json()
    return result;
  }
}

const getUserByUserName = async (username) => {
  const myHeaders = new Headers();
  myHeaders.append(
    "Authorization",
    `Bearer ${token}`);

  const requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
  };

  const response = await fetch(`${baseUrl}/api/users/${username}`, requestOptions)
  if (response.status === 200) {
    result = await response.json()
    return result;
  }
}

document.getElementById('uploadForm').addEventListener("submit", async function (e) {
  e.preventDefault();

  if (!this.checkValidity()) {
    this.reportValidity();
  }

  if (this.elements['file'].files.length === 0) {
      return;
  }

  if (this.elements['description'].value === '') {
      alert('Please, define description');
      return;
  }

  const file = this.elements['file'].files[0];
  const description = this.elements['description'].value;

  var data = new FormData();
  data.append('file', file);
  data.append('description', description);

  const requestOptions = {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`
    },
    redirect: 'follow',
    body: data
  };

  const response = await fetch(`${baseUrl}/api/documents/`, requestOptions)
  if (response.status == 201) {
    window.location = `/static/client_rest/documents.html`
  } else {
    alert("File upload error");
  }
});

const form = document.getElementById('searchForm');

form.addEventListener("submit", async (e) => {
  e.preventDefault()
  const searchValue = form.search_info.value
  if (searchValue) {
    const encodedSearchValue = encodeURIComponent(searchValue);
    window.location = `/static/client_rest/search_info.html?search=${encodedSearchValue}`;
  }
});

const form1 = document.getElementById('open_ai_form');

form1.addEventListener("submit", async (e) => {
  e.preventDefault()
  const openAiQuestion = form1.open_ai_form.value
  if (openAiQuestion) {
    const getAnswer = async () => {
      const myHeaders = new Headers();
      myHeaders.append(
        "Authorization",
        `Bearer ${token}`);

      const requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
      };

      const respons = await fetch(`${baseUrl}/api/openai/?data=${openAiQuestion}`, requestOptions)
      if (response.status == 200) {
        answerAi = await response.json()

        const message = encodeURIComponent(answerAi)
        window.location = `/static/client_rest/documents.html?message=${message}`
      }
    }
    getAnswer()
  }

});

const getDocuments = async () => {
  const myHeaders = new Headers();
  myHeaders.append(
    "Authorization",
    `Bearer ${token}`);

  const requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
  };

  const response = await fetch(`${baseUrl}/api/documents/?sort_by=date_added_desc`, requestOptions)
  if (response.status === 200) {
    result = await response.json();
    documents.innerHTML = "";

    for (const doc of result) {
      const documentUrl = document.createElement('a');
      documentUrl.href = doc.url;
      documentUrl.innerHTML = doc.url;
      const user = doc.user_id ? await getUserById(doc.user_id) : null;

      const el = document.createElement('div');
      el.className = 'modal-content rounded-4 shadow';

      const avatarUserNameDiv = document.createElement('div');
      avatarUserNameDiv.className = "author mb-2 mt-2"

      const authorLink = document.createElement('a');
      authorLink.className = 'author';
      authorLink.textContent = user.username;
      authorLink.href = `user_profile.html?username=${user.username}`
      avatarUserNameDiv.appendChild(authorLink);

      const docDiv = document.createElement('div');
      docDiv.appendChild(documentUrl);

      const documentsDescriptionDiv = document.createElement('div');
      documentsDescriptionDiv.className = "some_class mb-2"
      const descriptionSpan = document.createElement('span');
      descriptionSpan.textContent = doc.description;
      documentsDescriptionDiv.appendChild(descriptionSpan);

      const topicsDiv = document.createElement('div');
      topicsDiv.className = 'node__topics';
      topicsDiv.textContent = 'Tags: ';
      topicsDiv.textContent = 'Tags: ';

      if (document.tags) {
          for (const tag of document.tags) {
            const tagLink = document.createElement('a');
            tagLink.className = 'btn mb-2 mb-md-0 btn-outline-danger btn-sm';
            tagLink.textContent = tag.name;
            topicsDiv.appendChild(tagLink);
          }
          documentsDescriptionDiv.appendChild(topicsDiv)
      }

      el.appendChild(avatarUserNameDiv);
      el.appendChild(docDiv);
      el.appendChild(documentsDescriptionDiv);

      documents.appendChild(el);
    }
  }
}

getDocuments();

