async function predict() {

    const data = {
        pregnancies: parseFloat(document.getElementById("pregnancies").value),
        glucose: parseFloat(document.getElementById("glucose").value),
        blood_pressure: parseFloat(document.getElementById("bp").value),
        skin_thickness: parseFloat(document.getElementById("skin").value),
        insulin: parseFloat(document.getElementById("insulin").value),
        bmi: parseFloat(document.getElementById("bmi").value),
        dpf: parseFloat(document.getElementById("dpf").value),
        age: parseFloat(document.getElementById("age").value)
    };

    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    document.getElementById("result").innerText =
        result.result + " (Confidence: " + (result.confidence * 100).toFixed(2) + "%)";
}