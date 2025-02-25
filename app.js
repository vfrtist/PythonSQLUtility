cardItems = document.querySelectorAll('.card>div')


cardItems.forEach(item => {
    const section = item.closest('section')
    const index = Array.from(item.parentNode.children).indexOf(item)
    item.addEventListener('mouseenter', (e) => {
        section.querySelectorAll('.card').forEach(card => {
            card.children[index].classList.add('highlight')
        })
    })
    item.addEventListener('mouseleave', (e) => {
        section.querySelectorAll('.card').forEach(card => {
            card.children[index].classList.remove('highlight')
        })
    })
});