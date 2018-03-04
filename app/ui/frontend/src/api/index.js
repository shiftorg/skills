// Sample job data
// TODO (jaylamb20@gmail.com): Replace this stuff
// with actual calls to ES
const jobs = [
  {  
    id: 1,
    job_title: 'Sr. Software Engineer',
    skills: ['Angular', 'Git', 'Jenkins CI'],
    match: "91.5%"
  }, 
  {  
    id: 2,
    job_title: 'Data Scientist',
    skills: ['R', 'Pandas', 'Git'],
    match: "89.0%"
  }, 
  {
    id: 3,
    job_title: 'QA Engineer',
    skills: ['Jenkins CI', 'Groovy', 'Go'],
    match: "82.5%"
  },
  {
    id: 4,
    job_title: 'QA Engineer II',
    skills: ['Jenkins CI', 'Groovy', 'Go'],
    match: "82.4%"
  },
  {
    id: 5,
    job_title: 'QA Engineer III',
    skills: ['Jenkins CI', 'Groovy', 'Go'],
    match: "81.5%"
  }
]

// Function to go get the data. Could be replaced with
// ES calls later
// NOTE: exporting like this makes it available to our
// "Home" component
export function fetchJobDescriptions(num_jobs= 3) {  
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(jobs.slice(0, num_jobs))
    }, 300)
  })
}
