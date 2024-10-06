
document.querySelector('#loginForm').onsubmit = async (e) => {
    e.preventDefault()
    login = document.querySelector('#email')
    password = document.querySelector('#password')
    response = await fetch('http://109.237.99.125:5000/login', {
        method: 'POST',
        body: JSON.stringify({login: login.value, password: password.value})
    })
        let data = await response.json()
    if (data.code === 200) {
        location.replace("servers")
    }
}


