function submitQuery() {
    var companyName = document.getElementById('companyName').value.trim();
    if (companyName) {
        document.getElementById('submitButton').disabled = true;
        document.getElementById('researchingIndicator').style.display = 'block';
        document.getElementById('results').style.display = 'none';
        
        let dotCount = 0;
        const interval = setInterval(() => {
            dotCount = (dotCount + 1) % 4;
            const dots = '.'.repeat(dotCount);
            document.getElementById('researchingDots').textContent = `Researching${dots}`;
        }, 500);

        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ company_name: companyName })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                // Display the results
                document.getElementById('humanRightsPolicy').innerHTML = `Answer: ${data.humanRightsPolicy.answer || 'No data available'}
                <br>Explanation: ${data.humanRightsPolicy.explanation || 'No explanation available'}
                <br>Proof: ${data.humanRightsPolicy.source || 'No source available'}`;

                document.getElementById('esgTraining').innerHTML = `Answer: ${data.esgTraining.answer || 'No data available'}
                <br>Explanation: ${data.esgTraining.explanation || 'No explanation available'}
                <br>Proof: ${data.esgTraining.source || 'No source available'}`;

                document.getElementById('scope1Emissions').innerHTML = `Answer: ${data.scope1Emissions.answer || 'No data available'}
                <br>Explanation: ${data.scope1Emissions.explanation || 'No explanation available'}
                <br>Proof: ${data.scope1Emissions.source || 'No source available'}`;

                document.getElementById('results').style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to fetch data: ' + error.message);
        })
        .finally(() => {
            clearInterval(interval); // Stop the researching dots animation
            document.getElementById('submitButton').disabled = false;
            document.getElementById('researchingIndicator').style.display = 'none';
        });
    } else {
        alert('Please enter a valid company name.');
    }
    return false;
}