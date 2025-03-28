function togglePassword(inputId, iconId) {
    const passwordField = document.getElementById(inputId);
    const eyeIcon = document.getElementById(iconId);
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';

    passwordField.setAttribute('type', type);
    if (type === 'text') {
        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');  
    } else {
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');  
    }
}

function copyURL() {
    var copyText = document.getElementById("shareURL");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");
    alert("Copied the URL: " + copyText.value);
  }
  
  function shareWithFriend() {

    var friend = prompt("Enter your friend's username:");
    if (friend && friend.trim() !== "") {
      fetch("/check_user/" + encodeURIComponent(friend))
        .then(response => response.json())
        .then(data => {
          if (data.exists) {

            alert("Shared playlist link with " + friend + ":\n" + document.getElementById("shareURL").value);
          } else {
            
            var errorMsg = document.getElementById("errorMsg");
            errorMsg.textContent = "Username not found, try again!";
            errorMsg.style.display = "block";
            setTimeout(function() {
              errorMsg.style.display = "none";
            }, 3000);
          }
        })
        .catch(error => {
          console.error("Error checking user:", error);
          var errorMsg = document.getElementById("errorMsg");
          errorMsg.textContent = "An error occurred, please try again.";
          errorMsg.style.display = "block";
          setTimeout(function() {
            errorMsg.style.display = "none";
          }, 3000);
        });
    } else {
      alert("No friend's username entered. Please try again.");
    }
  }

  var deleteUrl = "";
  function showDeleteMiniwindow(playlistName, url) {
    deleteUrl = url; 
    document.getElementById("MiniwindowText").textContent = "Are you sure you want to delete the playlist '" + playlistName + "'?";
    document.getElementById("deleteConfirm").style.display = "block";
  }
  
  function closeConfirm() {
    document.getElementById("deleteConfirm").style.display = "none";
  }
  
  function noDeletion() {
    document.getElementById("deleteConfirm").style.display = "none";
  }
  
  function confirmDeletion() {
    window.location.href = deleteUrl;
  }
  
  setTimeout(function(){
    var notif = document.getElementById("notification");
    if (notif) {
      notif.style.display = "none";
    }
  }, 3000);
  

  document.addEventListener('play', function(e) {
    const audios = document.getElementsByTagName('audio');
    for (let i = 0; i < audios.length; i++) {
      if (audios[i] !== e.target) {
        audios[i].pause();
      }
    }
  }, true);
  
  function copyURL() {
    var copyText = document.getElementById("shareURL");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");
    alert("Copied the URL: " + copyText.value);
  }

  function openMiniwindow() { 
    document.getElementById("friendMiniwindow").style.display = "block"; 
    document.getElementById("miniwindowError").innerText = ""; 
    document.getElementById("friendInput").value = "";
  }
  
  function closeMiniwindow() {
    document.getElementById("friendMiniwindow").style.display = "none"; 
  }
  
  function submitFriend() {
    var friendUsername = document.getElementById("friendInput").value.trim();
    if (!friendUsername) {
      document.getElementById("miniwindowError").innerText = "Please enter a username.";
      return;
    }
    fetch(`/check_user/${friendUsername}`)
      .then(response => response.json())
      .then(data => {
        if (data.exists) {
          let currentUrl = new URL(document.getElementById("shareURL").value);
          currentUrl.searchParams.set("friend_username", friendUsername);
          window.location.href = currentUrl.toString();
        } else {
          document.getElementById("miniwindowError").innerText = "Username not found, try again.";
        }
      })
      .catch(error => {
        console.error('Error checking friend username:', error);
        document.getElementById("miniwindowError").innerText = "An error occurred, please try again.";
      });
  }
  
  // NEW: copyURL function for copying the share URL
  function copyURL() {
    var shareInput = document.getElementById("shareURL");
    shareInput.select();
    shareInput.setSelectionRange(0, 99999); // For mobile devices
  
    navigator.clipboard.writeText(shareInput.value).then(() => {
      alert("URL copied to clipboard!");
    }).catch(err => {
      console.error("Failed to copy URL:", err);
      alert("Failed to copy URL");
    });
  }
  
  window.onclick = function(event) {
    var miniWindow = document.getElementById("friendMiniwindow");
    if (event.target == miniWindow) { 
      closeMiniwindow(); 
    }
  }
  