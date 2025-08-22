let currentStep = 1;

function showStep(step) {
  document.querySelectorAll('.step').forEach((el, idx) => {
    el.style.display = (idx + 1 === step) ? 'block' : 'none';
  });
  document.getElementById('currentStepNum').innerText = step;

  // Update progress bar
  const totalSteps = document.querySelectorAll('.step').length;
  const progressPercent = (step / totalSteps) * 100;
  document.getElementById('progressBar').style.width = progressPercent + '%';
}

// Validate fields before moving to next step
function validateStep(step) {
  const stepDiv = document.getElementById(`step${step}`);
  const inputs = stepDiv.querySelectorAll('input, select');
  for (let i = 0; i < inputs.length; i++) {
    if (!inputs[i].checkValidity()) {
      inputs[i].reportValidity(); // highlight first invalid
      return false;
    }
  }
  return true;
}

function nextStep(step) {
  if (validateStep(step)) {
    currentStep = step + 1;
    showStep(currentStep);
  }
}

function prevStep(step) {
  currentStep = step - 1;
  showStep(currentStep);
}

// Password confirmation check
function validateStep3() {
  const password = document.getElementById("password").value;
  const confirm = document.getElementById("confirm_password").value;
  if (!password || !confirm) {
    alert("Please fill both password fields!");
    return false;
  }
  if (password !== confirm) {
    alert("Passwords do not match!");
    return false;
  }
  return true;
}

// Attach validation to final submit
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#step3 button[type='submit']").onclick = function(e) {
    if (!validateStep3()) e.preventDefault();
  };

  // Initialize first step
  showStep(currentStep);
});
