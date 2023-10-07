token = localStorage.getItem("accessToken")

documents = document.getElementById("documents")

////const baseUrl = 'https://svitlogram.fly.dev';
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
    const result = await response.json()
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

  const response = await requestApi(`${baseUrl}/api/users/${username}`, requestOptions)
  if (response.status === 200) {
    const result = await response.json()
    return result;
  }
}
const uploadForm = document.getElementById('uploadForm');

uploadForm.addEventListener("submit", async function (e) {
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

  const response = await requestApi(`${baseUrl}/api/documents/`, requestOptions)
  if (response.status == 201) {
    window.location = `/static/client_rest/documents.html`
  } else {
    alert("File upload error");
  }
});

const getDocuments = async () => {
  const myHeaders = new Headers();
  myHeaders.append(
    "Authorization",
    `Bearer ${token}`);

  const requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };

  const response = await requestApi(`${baseUrl}/api/documents/?sort_by=date_added_desc`, requestOptions)
  if (response.status === 200) {
    const result = await response.json();
    documents.innerHTML = "";

    for (const doc of result) {
      const user = doc.user_id ? await getUserById(doc.user_id) : null;

      const documentUrl = document.createElement('a');
      documentUrl.href = doc.url;
      documentUrl.innerHTML = "Download";

      const docDiv = document.createElement('div');
      docDiv.appendChild(documentUrl);

      const chatLink = document.createElement('a');
      chatLink.className = 'chat';
      chatLink.textContent = doc.description;
      chatLink.href = '#'
      chatLink.setAttribute('data-doc-id', doc.id);

      const avatarUserNameDiv = document.createElement('div');
      avatarUserNameDiv.className = "author mb-2 mt-2"
      avatarUserNameDiv.appendChild(chatLink);

      const documentsDescriptionDiv = document.createElement('div');
      documentsDescriptionDiv.className = "some_class mb-2"

      const listItem = document.createElement('div');
      listItem.className = 'list-group-item';

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

      listItem.appendChild(avatarUserNameDiv);
      listItem.appendChild(docDiv);
      listItem.appendChild(documentsDescriptionDiv);

      documents.appendChild(listItem);
    }
    if (result.length === 5) {
        uploadForm.setAttribute("hidden", "hidden");
    }
  }
}

$(document.body).on('click', '.chat', async function(e) {
    const docId = $(this).data('doc-id');

    $('#chatMessages').data('doc-id', docId).empty();
    $('#chatContainer').removeAttr('hidden');
    $('#selectDocumentMessage').attr('hidden', true);

    await loadChatHistory(docId);
});

const loadChatHistory = async function (docId) {
  const requestOptions = {
    method: 'GET',
    headers: {
        "Authorization": `Bearer ${token}`
    },
    redirect: 'follow'
  };

  const response = await fetch(`${baseUrl}/api/documents/chats/?document_id=${docId}&skip=0&limit=1000`, requestOptions)
  if (response.status === 200) {
    const result = await response.json();

    for (let i in result) {
        printChatMessage(result[i].question);
        printChatMessage(result[i].answer);
    }
  }
}

$('#sendMessageForm').on('submit', async function(e) {
    e.preventDefault();

    var $messageInput = $('#messageInput');
    var messageText = $messageInput.val();

    const documentId = $('#chatMessages').data('doc-id');

    if (messageText.trim().length >= 5) {
        printChatMessage(messageText);
        $messageInput.val('');

        await sendMessage(documentId, messageText);
    }
});

const printChatMessage = function (messageText) {
    var $chatMessages = $('#chatMessages');

    var $li = $('<li>');
    $li.addClass('mb-2');
    $li.html(messageText);
    $chatMessages.append($li);
}

const sendMessage = async function (documentId, question) {
    const requestOptions = {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    redirect: 'follow',
    body: JSON.stringify({question})
  };

  const response = await fetch(`${baseUrl}/api/documents/chats/?document_id=${documentId}`, requestOptions)
  if (response.status === 201) {
    const result = await response.json();
    printChatMessage(result.answer);
  }
};

getDocuments();
