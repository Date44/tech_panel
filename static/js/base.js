async function fetchData() {
    const response = await fetch('http://109.237.99.125:5000/data', {
        method: 'POST',
    });
    const data = await response.json();
    console.log(data);
}

fetchData();

