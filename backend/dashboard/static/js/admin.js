console.log("Admin JS loaded");

document.querySelector(".side-nav__exams").addEventListener("click", (e) => {
    document.querySelector(".main").style.display = "none";
    document.querySelector(".user-section").style.display = "none";
    document.querySelector(".order-section").style.display = "none";
    document.querySelector(".account-section").style.display = "none";
    document.querySelector(".exam-section").style.display = "block";
  });
  document.querySelector(".side-nav__users").addEventListener("click", (e) => {
    document.querySelector(".main").style.display = "none";
    document.querySelector(".user-section").style.display = "block";
    document.querySelector(".order-section").style.display = "none";
    document.querySelector(".account-section").style.display = "none";
    document.querySelector(".exam-section").style.display = "none";
  });
  document.querySelector(".side-nav__orders").addEventListener("click", (e) => {
    document.querySelector(".main").style.display = "none";
    document.querySelector(".user-section").style.display = "none";
    document.querySelector(".order-section").style.display = "block";
    document.querySelector(".account-section").style.display = "none";
    document.querySelector(".exam-section").style.display = "none";
  });
  document.querySelector(".side-nav__account").addEventListener("click", (e) => {
    document.querySelector(".main").style.display = "none";
    document.querySelector(".user-section").style.display = "none";
    document.querySelector(".order-section").style.display = "none";
    document.querySelector(".account-section").style.display = "block";
    document.querySelector(".exam-section").style.display = "none";
  });
  
  document.querySelector(".btn--new").addEventListener("click", (e) => {
    document.querySelector(".exam-section").style.display = "none";
    document.querySelector(".new--exam_container").style.display = "block";
  });
  
  document
    .querySelector(".exam-section .exam-container .values a")
    .addEventListener("click", (e) => {
      document.querySelector(".exam-section").style.display = "none";
      document.querySelector(".update--exam_container").style.display =
        "block";
    });
  
  document
    .querySelector(".user-section .user--new .btn--new")
    .addEventListener("click", (e) => {
      document.querySelector(".user-section").style.display = "none";
      document.querySelector(".new--user_container").style.display = "block";
    });
  
  document
    .querySelector(".user-section .user-container .values a")
    .addEventListener("click", (e) => {
      document.querySelector(".user-section").style.display = "none";
      document.querySelector(".update--user_container").style.display = "block";
    });
  
  document
    .querySelector(".new--exam_header .back--btn")
    .addEventListener("click", (e) => {
      document.querySelector(".exam-section").style.display = "block";
      document.querySelector(".new--exam_container").style.display = "none";
    });
  
  document
    .querySelector(".update--exam_header .back--btn")
    .addEventListener("click", (e) => {
      document.querySelector(".exam-section").style.display = "block";
      document.querySelector(".update--exam_container").style.display = "none";
    });
  
  document
    .querySelector(".new--user_header .back--btn")
    .addEventListener("click", (e) => {
      document.querySelector(".user-section").style.display = "block";
      document.querySelector(".new--user_container").style.display = "none";
    });
  
  document
    .querySelector(".update--user_header .back--btn")
    .addEventListener("click", (e) => {
      document.querySelector(".user-section").style.display = "block";
      document.querySelector(".update--user_container").style.display = "none";
    });