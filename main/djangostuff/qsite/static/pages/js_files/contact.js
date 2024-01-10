const openContactButtons = document.querySelectorAll('[data-contact-target]')
const closeContactButtons = document.querySelectorAll('[data-close-button]')

openContactButtons.forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault()
        const modal = document.querySelector(link.dataset.contactTarget)
        openContact(modal)
    })
})

closeContactButtons.forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault()
        const modal = link.closest('.contact')
        closeContact(modal)
    })
})

function openContact(contact) {
    if (contact == null) return
    contact.classList.add('active')
}

function closeContact(contact) {
    if (contact == null) return
    contact.classList.remove('active')
}
