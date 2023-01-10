
function post_object() {
  object_id = document.getElementById("inputObjectId").value
  fetch('/jobs', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ object_id: object_id }),
  })
  .then(response => response.json())
  .then(data => {
    getJobStatusById(data.job_id)
  })
}

function getJobDetails() {
  job_id = document.getElementById("inputJobId").value
  fetch(`/jobs/${job_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(res => {
    const html = `
      <tr>
        <td>${res.id}</td>
        <td>${res.object_id}</td>
        <td>${res.timestamp}</td>
        <td>${res.duration}</td>
        <td>${res.status}</td>
      </tr>`;
    document.getElementById('job').innerHTML = html
  })
  .catch(err => console.log(err));
}

function getJobStatusById(job_id) {
  fetch(`/jobs/${job_id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(res => {
    const html = `
      <tr>
        <td>${res.id}</td>
        <td>${res.object_id}</td>
        <td>${res.timestamp}</td>
        <td>${res.status}</td>
      </tr>`;
    const newRow = document.getElementById('jobs').insertRow(0);
    newRow.innerHTML = html;
    document.getElementById("inputJobId").value = res.id
  })
  .catch(err => console.log(err));
}

