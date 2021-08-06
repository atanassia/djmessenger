const alertBox = document.getElementById('alert-box')

const form = document.getElementById('sending-form')

const messsage = document.getElementById('inputMessage')

const csrf = document.getElementsByName('csrfmiddlewaretoken')
console.log(csrf)

const url = ""

const handleAlerts = (type, text) =>{
    alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
                            ${text}
                        </div>`
}

form.addEventListener('submit', e=>{
    e.preventDefault()

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('message', message.value)

    $.ajax({
        type: 'POST',
        url: url,
        data: fd,
        success: function(response){
            console.log(response)
            const sText = `successfully saved ${response.message}`
            handleAlerts('success', sText)
            setTimeout(()=>{
                alertBox.innerHTML = ""
                message.innerHTML = ""
            }, 3000)
        },
        error: function(error){
            console.log(error)
            handleAlerts('danger', 'ups..something went wrong')
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})

console.log(form)