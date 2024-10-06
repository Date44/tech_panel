async function fetchData() {
    const response = await fetch('http://127.0.0.1:5000/data', {
        method: 'POST',
    });
    const data = await response.json();
    console.log(data);
}

fetchData();

