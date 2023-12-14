const prepend = "/api/"
function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function customFormWrapper(e) {
    e.preventDefault();
    customFormHandler(e);
}

document.addEventListener("submit", customFormWrapper);

function sendForm(endpoint,formBody){
    fetch(endpoint, {
        method: "POST",
        body: formBody,
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then((response) =>
        response.json()
    )
    .then((json) => {
        console.log(json)
        switch (json.status) {
            case 406:
            case 500:
                showMessage(json.mensaje)
                break;
            case 301:
                showMessage("Logged in, redirecting to the dashboard...",0)
                form.action = prepend.substring(0,prepend.length-1)+json.target
                form.submit()
                break;
            case 200:
                showMessage(json.mensaje,0)
                if (endpoint.split("/").pop() != "password"){
                    loadForm()
                }
            break;
        }
    });
}
function globalMain(){
    main();
}