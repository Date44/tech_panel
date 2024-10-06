
document.querySelector('#loginForm').onsubmit = async (e) => {
    e.preventDefault()
    email = document.querySelector('#email')
    password = document.querySelector('#password')
    response = await fetch('http://109.237.99.125:5000/login', {
        method: 'POST',
        body: JSON.stringify({email: email.value, password: password.value})
    })
        let data = await response.json()
    console.log(data)
}


