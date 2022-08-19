document.addEventListener("DOMContentLoaded", () => {
  const info_head_color = "{{ infoStatus }}"
  if (info_head_color === 'fail') {
    document.querySelector(".infoCard").style.borderTopColor = 'red'
  }
})