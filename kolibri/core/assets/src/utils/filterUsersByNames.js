import Fuse from 'fuse.js';

// Filters array of FacilityUser objects based on their `username` or `full_name` fields
export default function filterUsersByNames(users, searchTerm) {
  const searcher = new Fuse(users, {
    threshold: 0.1,
    keys: [
      'username',
      // NOTE: `name` is used as an alias to `full_name` in e.g. IndividualLearnerSelector
      {
        name: 'name',
        weight: 2,
      },
      {
        name: 'full_name',
        weight: 2,
      },
      {
        name: 'user_name',
        weight: 3,
      },
      {
        name: 'learner_name',
        weight: 4,
      },
      {
        name: 'mentee',
        weight: 5,
      },
      {
        name: 'mentor',
        weight: 6,
      },
    ],
  });
  if (searchTerm) {
    return searcher.search(searchTerm).map(x => x.item);
  } else {
    return users;
  }
}
