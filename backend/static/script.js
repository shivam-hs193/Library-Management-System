const API = "http://127.0.0.1:5000";

function addBook() {
    fetch(`${API}/add-book`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            title: title.value,
            author: author.value,
            publisher: publisher.value,
            year: year.value,
            category: category.value,
            copies: copies.value
        })
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}

function addMember() {
    fetch(`${API}/add-member`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: mname.value,
            email: email.value,
            phone: phone.value
        })
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}

function issueBook() {
    fetch(`${API}/issue-book`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            book_id: ibook.value,
            member_id: imember.value
        })
    })
    .then(res => res.json())
    .then(data => alert(JSON.stringify(data)));
}

function returnBook() {
    fetch(`${API}/return-book`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            transaction_id: transaction.value
        })
    })
    .then(res => res.json())
    .then(data => alert(`Fine: ₹${data.fine}`));
}

function loadBooks() {
    fetch(`${API}/available-books`)
        .then(res => res.json())
        .then(data => {
            books.innerHTML = "";
            data.forEach(b => {
                books.innerHTML += `
                    <tr>
                        <td>${b.book_id}</td>
                        <td>${b.title}</td>
                        <td>${b.author}</td>
                        <td>${b.available_copies}</td>
                    </tr>`;
            });
        });
}
