/* 크리스천도 불안할 수 있습니다 — 랜딩 인터랙션 */
(function () {
  "use strict";

  /* ---- 네비게이션: 스크롤 시 배경 ---- */
  var nav = document.getElementById("nav");
  function onScroll() {
    if (window.scrollY > 24) nav.classList.add("scrolled");
    else nav.classList.remove("scrolled");
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---- 모바일 메뉴 토글 ---- */
  var toggle = document.getElementById("navToggle");
  var links = document.getElementById("navLinks");
  toggle.addEventListener("click", function () {
    links.classList.toggle("open");
    nav.classList.toggle("menu-open");
  });
  links.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", function () {
      links.classList.remove("open");
      nav.classList.remove("menu-open");
    });
  });

  /* ---- 스크롤 리빌 ---- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("visible"); });
  }

  /* ===========================================================
     자가진단 (빈도 척도 0~3 × 6문항 = 0~18점)
     =========================================================== */
  var quiz = document.getElementById("quiz");
  if (quiz) {
    var TOTAL_Q = 6;
    var progressBar = document.getElementById("quizProgress");
    var answeredEl = document.getElementById("quizAnswered");
    var hint = document.getElementById("quizHint");
    var submit = document.getElementById("quizSubmit");
    var result = document.getElementById("result");

    function answeredCount() {
      var n = 0;
      for (var i = 1; i <= TOTAL_Q; i++) {
        if (quiz.querySelector('input[name="q' + i + '"]:checked')) n++;
      }
      return n;
    }

    quiz.addEventListener("change", function () {
      var n = answeredCount();
      answeredEl.textContent = n;
      progressBar.style.width = (n / TOTAL_Q * 100) + "%";
      if (n === TOTAL_Q) hint.hidden = true;
    });

    var BANDS = [
      { min: 0,  label: "안정",   color: "#6aa57a",
        title: "지금은 비교적 안정적인 상태로 보여요",
        body: "큰 어려움 없이 불안을 다루고 계신 것 같아요. 그래도 마음이 무거운 날이 찾아온다면 혼자 견디지 마세요. 이 책은 불안을 더 깊이 이해하고 미리 돌보는 데 좋은 길동무가 되어 줄 거예요." },
      { min: 5,  label: "경도",   color: "#8fb3da",
        title: "가벼운 불안 신호가 보여요",
        body: "아직 큰 문제는 아니지만, 불안이 조금씩 신호를 보내고 있어요. 지금이 나를 이해하고 돌보기 시작하기 가장 좋은 때예요. 책의 '몸·마음·영혼' 통합 접근이 도움이 될 거예요." },
      { min: 10, label: "중등도", color: "#b3a3d6",
        title: "불안이 일상에 또렷이 영향을 주고 있어요",
        body: "불안이 수면·집중·관계 등 일상에 또렷한 영향을 주고 있는 것 같아요. 이것은 당신이 약하거나 믿음이 부족하다는 뜻이 아니라, 돌봄이 필요하다는 신호예요. 책과 함께, 그리고 필요하다면 전문가와 함께 회복을 시작해 보세요." },
      { min: 15, label: "높음",   color: "#d9714e",
        title: "불안 수준이 상당히 높은 편이에요",
        body: "불안이 삶의 여러 영역을 무겁게 누르고 있는 것 같아요. 결코 당신의 잘못이 아닙니다. 자책을 내려놓고, 가능한 한 빨리 정신건강 전문가의 도움을 받아 보시길 권해요. 이 책이 그 길의 정직한 안내자가 되어 줄 거예요." }
    ];

    function bandFor(score) {
      var b = BANDS[0];
      for (var i = 0; i < BANDS.length; i++) if (score >= BANDS[i].min) b = BANDS[i];
      return b;
    }

    submit.addEventListener("click", function () {
      if (answeredCount() < TOTAL_Q) { hint.hidden = false; return; }
      hint.hidden = true;

      var score = 0;
      for (var i = 1; i <= TOTAL_Q; i++) {
        score += parseInt(quiz.querySelector('input[name="q' + i + '"]:checked').value, 10);
      }
      var band = bandFor(score);

      document.getElementById("resultNum").textContent = score;
      var bandEl = document.getElementById("resultBand");
      bandEl.textContent = "불안 수준 · " + band.label;
      bandEl.style.background = band.color;
      document.getElementById("resultTitle").textContent = band.title;
      document.getElementById("resultBody").textContent = band.body;

      result.hidden = false;
      // 미터 애니메이션
      var meter = document.getElementById("resultMeter");
      meter.style.width = "0%";
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { meter.style.width = (score / 18 * 100) + "%"; });
      });
      result.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  }

  /* ===========================================================
     문의 모달
     =========================================================== */
  var modal = document.getElementById("modal");
  if (modal) {
    var modalForm = document.getElementById("modalForm");
    var modalDone = document.getElementById("modalDone");
    var inquiryForm = document.getElementById("inquiryForm");
    var formError = document.getElementById("formError");

    function openModal() {
      modalForm.hidden = false;
      modalDone.hidden = true;
      formError.hidden = true;
      inquiryForm.reset();
      modal.hidden = false;
      document.body.classList.add("modal-open");
    }
    function closeModal() {
      modal.hidden = true;
      document.body.classList.remove("modal-open");
    }

    document.querySelectorAll("[data-open-form]").forEach(function (btn) {
      btn.addEventListener("click", openModal);
    });
    modal.querySelectorAll("[data-close]").forEach(function (el) {
      el.addEventListener("click", closeModal);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !modal.hidden) closeModal();
    });

    inquiryForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = inquiryForm;
      var ok = f.name.value.trim() && f.phone.value.trim() && f.message.value.trim() && f.agree.checked;
      if (!ok) { formError.hidden = false; return; }
      // 시연: 실제 전송 없이 완료 화면 표시
      modalForm.hidden = true;
      modalDone.hidden = false;
    });
  }
})();
