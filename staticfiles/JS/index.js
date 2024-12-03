$(document).ready(function() {
    $('#jobPostingsTable').DataTable({
        pageLength: 5, // Initial page length
        order: [[4, 'desc']],   // Sort by date by default
        language: {
            search: "",
            searchPlaceholder: 'Search jobs...',
            lengthMenu: "Show _MENU_entries",
            paginate: {
                first: '<i class="fa fa-angle-double-left"></i>',
                last: '<i class="fa fa-angle-double-right"></i>',
                next: '<i class="fa fa-angle-right"></i>',
                previous: '<i class="fa fa-angle-left"></i>'
            }
        },
        lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ], // Define the options for the length menu
        columnDefs: [
            { orderable: false, targets: 5 } // Disable sorting for actions column
        ]
    });
});


$(document).ready(function() {
    $('#companyverifiedTable').DataTable({
        pageLength: 5, // Initial page length
        order: [[4, 'desc']],   // Sort by date by default
        language: {
            search: "",
            searchPlaceholder: 'Search jobs...',
            lengthMenu: "Show _MENU_entries",
            paginate: {
                first: '<i class="fa fa-angle-double-left"></i>',
                last: '<i class="fa fa-angle-double-right"></i>',
                next: '<i class="fa fa-angle-right"></i>',
                previous: '<i class="fa fa-angle-left"></i>'
            }
        },
        lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ], // Define the options for the length menu
        columnDefs: [
            { orderable: false, targets: 5 } // Disable sorting for actions column
        ]
    });
  });



$(document).ready(function() {
    $('#jobApplicationStatusTable').DataTable({
        pageLength: 5, // Initial page length
        order: [[2,'desc']],   // Sort by date by default
        language: {
            search: "",
            searchPlaceholder: 'Search jobs...',
            lengthMenu: "Show _MENU_entries",
            paginate: {
                first: '<i class="fa fa-angle-double-left"></i>',
                last: '<i class="fa fa-angle-double-right"></i>',
                next: '<i class="fa fa-angle-right"></i>',
                previous: '<i class="fa fa-angle-left"></i>'
            }
        },
        lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ], // Define the options for the length menu
        columnDefs: [
            { orderable: false, targets: 4 } // Disable sorting for actions column
        ]
    });
});


$(document).ready(function() {
    $('#jobfairPostingsTable').DataTable({
        pageLength: 5, // Initial page length
        order: [[4, 'desc']],   // Sort by date by default
        language: {
            search: "",
            searchPlaceholder: 'Search job fairs...',
            lengthMenu: "Show _MENU_entries",
            paginate: {
                first: '<i class="fa fa-angle-double-left"></i>',
                last: '<i class="fa fa-angle-double-right"></i>',
                next: '<i class="fa fa-angle-right"></i>',
                previous: '<i class="fa fa-angle-left"></i>'
            }
        },
        lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ], // Define the options for the length menu
        columnDefs: [
            { orderable: false, targets: 5 } // Disable sorting for actions column
        ]
    });
});

$(document).ready(function() {
    $('#jobSavedTable').DataTable({
        pageLength: 5, // Initial page length
        order: [[2, 'desc']],   // Sort by date by default
        language: {
            search: "",
            searchPlaceholder: 'Search saved job...',
            lengthMenu: "Show _MENU_entries",
            paginate: {
                first: '<i class="fa fa-angle-double-left"></i>',
                last: '<i class="fa fa-angle-double-right"></i>',
                next: '<i class="fa fa-angle-right"></i>',
                previous: '<i class="fa fa-angle-left"></i>'
            }
        },
        lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ], // Define the options for the length menu
        columnDefs: [
            { orderable: false, targets: 3 } // Disable sorting for actions column
        ]
    });
});

$(document).ready(function() {
    $('#applicationAnalyticsTable').DataTable({
        pageLength: 3, // Initial page length
        order: [[2, 'desc']],   // Sort by date by default
        language: {
            search: "",
            searchPlaceholder: 'Search jobs...',
            lengthMenu: "Show _MENU_entries",
            paginate: {
                first: '<i class="fa fa-angle-double-left"></i>',
                last: '<i class="fa fa-angle-double-right"></i>',
                next: '<i class="fa fa-angle-right"></i>',
                previous: '<i class="fa fa-angle-left"></i>'
            }
        },
        lengthMenu: [ [3, 5, 10, 25, 50, -1], [3, 5, 10, 25, 50, "All"] ], // Define the options for the length menu
        columnDefs: [
            { orderable: false, targets: 3 } // Disable sorting for actions column
        ]
    });
});

$(document).ready(function() {
    $('#jobAnalyticsTable').DataTable({
        pageLength: 3, // Initial page length
        order: [[2, 'desc']],   // Sort by date by default
        language: {
            search: "",
            searchPlaceholder: 'Search jobs...',
            lengthMenu: "Show _MENU_entries",
            paginate: {
                first: '<i class="fa fa-angle-double-left"></i>',
                last: '<i class="fa fa-angle-double-right"></i>',
                next: '<i class="fa fa-angle-right"></i>',
                previous: '<i class="fa fa-angle-left"></i>'
            }
        },
        lengthMenu: [ [3, 5, 10, 25, 50, -1], [3, 5, 10, 25, 50, "All"] ], // Define the options for the length menu
        columnDefs: [
            { orderable: false, targets: 3 } // Disable sorting for actions column
        ]
    });
});

$(document).ready(function() {
    $('#jobFairTable').DataTable({
        pageLength: 5, // Initial page length
        order: [[2, 'desc']],   // Sort by date by default
        language: {
            search: "",
            searchPlaceholder: 'Search job fairs...',
            lengthMenu: "Show _MENU_entries",
            paginate: {
                first: '<i class="fa fa-angle-double-left"></i>',
                last: '<i class="fa fa-angle-double-right"></i>',
                next: '<i class="fa fa-angle-right"></i>',
                previous: '<i class="fa fa-angle-left"></i>'
            }
        },
        lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ], // Define the options for the length menu
        columnDefs: [
            { orderable: false, targets: 3 } // Disable sorting for actions column
        ]
    });
});


// ============== Scroll to Top ================ //
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
    }

    window.addEventListener('scroll', function() {
    var scrollButton = document.getElementById('scroll-to-top');
    if (window.scrollY > 300) {
        scrollButton.style.display = 'block';
    } else {
        scrollButton.style.display = 'none';
    }
});
  
// ============== End of Scroll to Top ================ //


const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

// GO TO FIND JOBS Homepage
document.getElementById("findjobs-link").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the default anchor click behavior
    const findJobsSection = document.getElementById("findjobs");
    
    // Adjust the scroll position with a smooth scroll effect
    window.scrollTo({
        top: findJobsSection.offsetTop - 150, // Adjust based on the navbar height
        behavior: 'smooth'
    });
});

// END OF GO TO FIND JOBS Homepage



document.getElementById("filter-btn").addEventListener("click", function() {
    const filterOptions = document.getElementById("filter-options");
    const mainHeading = document.getElementById("main-heading");
    const subHeading = document.getElementById("sub-heading");
    
    filterOptions.classList.toggle("filter-hidden");
    filterOptions.classList.toggle("filter-visible");

    mainHeading.classList.toggle("d-none");
    subHeading.classList.toggle("d-none");
});

function showJobDetails(jobId) {
    // Remove 'active' class from all job cards and hide all job details
    document.querySelectorAll('.job-card').forEach(card => {
        card.classList.remove('active');
    });
    document.querySelectorAll('.job-details').forEach(detail => {
        detail.classList.remove('active');
    });

    // Add 'active' class to the clicked job card and display corresponding job details
    document.querySelector(`.job-card[onclick="showJobDetails(${jobId})"]`).classList.add('active');
    document.getElementById(`job-${jobId}`).classList.add('active');
}

function showInboxDetails(inboxId) {
    // Remove 'active' class from all job cards and hide all job details
    document.querySelectorAll('.inbox-card').forEach(card => {
        card.classList.remove('active');
    });
    document.querySelectorAll('.inbox-details').forEach(detail => {
        detail.classList.remove('active');
    });

    // Add 'active' class to the clicked inbox card and display corresponding inbox details
    document.querySelector(`.inbox-card[onclick="showInboxDetails(${inboxId})"]`).classList.add('active');
    const activeInboxDetail = document.getElementById(`inbox-${inboxId}`);
    activeInboxDetail.classList.add('active');

    // Scroll to the bottom of the messages container
    const messagesContainer = activeInboxDetail.querySelector('.messages-container');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}


// JavaScript to manage the step flow
let currentStep = 1;

function nextStep(step) {
    if (validateStep(step)) {
        // Hide current step
        document.getElementById('step' + step).classList.add('d-none');
        // Show next step
        document.getElementById('step' + (step + 1)).classList.remove('d-none');
        currentStep = step + 1;

        // Show the navigation buttons once we're past step 1
        if (currentStep > 1) {
            document.getElementById('navigationButtons').classList.remove('d-none');
        }
    }
}

function previousStep() {
    // Hide current step
    document.getElementById('step' + currentStep).classList.add('d-none');
    // Show previous step
    document.getElementById('step' + (currentStep - 1)).classList.remove('d-none');
    currentStep -= 1;

    // Hide the "Previous" button if we're on the first step
    if (currentStep === 1) {
        document.getElementById('navigationButtons').classList.add('d-none');
    }
}

function validateStep(step) {
    // Simple validation for required fields
    const inputs = document.querySelectorAll(`#step${step} input`);
    for (let input of inputs) {
        if (!input.checkValidity()) {
            input.reportValidity();
            return false;
        }
    }
    return true;
}

// Function to clone and add a skill input field
function addSkill() {
    let container = document.getElementById('skills-container');
    let newSkill = document.querySelector('.skill-item').cloneNode(true);
    newSkill.querySelector('input').value = ''; // Clear input value
    container.appendChild(newSkill);
}

// Function to clone and add a responsibility input field
function addResponsibility() {
    let container = document.getElementById('responsibilities-container');
    let newResponsibility = document.querySelector('.responsibility-item').cloneNode(true);
    newResponsibility.querySelector('input').value = ''; // Clear input value
    container.appendChild(newResponsibility);
}

// Function to clone and add an experience input field
function addExperience() {
    let container = document.getElementById('experiences-container');
    let newExperience = document.querySelector('.experience-item').cloneNode(true);
    newExperience.querySelector('input').value = ''; // Clear input value
    container.appendChild(newExperience);
}