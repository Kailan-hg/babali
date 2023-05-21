url = window.location.href
if(/\/product\/maker/ig){
    document.querySelector('[name="company_name"]').value = url.split("company_name=").pop().split("&").shift().trim()
}