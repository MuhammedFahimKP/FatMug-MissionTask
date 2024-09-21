const form = document.getElementById("form");
const video = document.getElementById("video");
const input = document.getElementById("searchBox");
const videoID = video.getAttribute("data-video-id");
const fetchUrl = video.getAttribute("data-video-url");
const timelineListContainer = document.getElementById("timelineList");
const timeLinks = document.getElementsByClassName("time-link");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const query = input.value;
  fetch(fetchUrl + `?query=${query}`, {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      removeChildofTimeLine();

      if (data?.length > 0) {
        data.forEach((item) => {
          const timelineDiv = document.createElement("div");
          timelineDiv.className = "comment mb-2";
          timelineDiv.innerHTML = `<p class="link-primary" onclick="clickingTheTimeLink(event)"  style="text-decoration: underline:" data-time="${item}" >${item}</p>`;

          timelineListContainer.appendChild(timelineDiv);
        });
      }

      if (data?.length == 0) {
        timelineListContainer.innerHTML = `<p class="text-danger"> no items found for ${query} </p>`;
      }

      if (data?.video) {
        timelineListContainer.innerHTML = `<p class="text-danger"> video doesn't have subtitles </p>`;
      }
    });
});

function convertTimeToSeconds(timeString) {
  // Split the time string into components [HH, MM, SS.mmm]
  const [hours, minutes, seconds] = timeString.split(":");

  // Convert each component to a number and calculate the total seconds
  const hoursInSeconds = parseInt(hours, 10) * 3600;
  const minutesInSeconds = parseInt(minutes, 10) * 60;
  const secondsFloat = parseFloat(seconds);

  // Return the total time in seconds
  return hoursInSeconds + minutesInSeconds + secondsFloat;
}

function clickingTheTimeLink(event) {
  // Check if the clicked element is a <p> with the class 'timestamp'
  // Get the time value from the data-time attribute of the clicked <p>
  const time = event.target.getAttribute("data-time");

  // Set the current time of the video player and play the video

  video.currentTime = convertTimeToSeconds(time); // Set the video to the clicked time
  video.play(); // Start playing the video
}

function removeChildofTimeLine() {
  if (timelineListContainer.hasChildNodes()) {
    timelineListContainer.innerHTML = "";
  }
}
