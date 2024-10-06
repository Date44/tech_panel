response = fetch('http://127.0.0.1:5000/data', {
method: 'POST',
}).then(res => res.json())
console.log(response)
