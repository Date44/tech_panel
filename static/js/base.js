response = fetch('http://localhost:5000/data', {
method: 'POST',
}).then(res => res.json())
console.log(response)
