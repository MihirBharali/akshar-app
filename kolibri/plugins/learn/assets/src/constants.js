// a name for every URL pattern
export const PageNames = {
  ROOT: 'ROOT',
  TOPICS_ROOT: 'TOPICS_ROOT',
  TOPICS_CHANNEL: 'TOPICS_CHANNEL',
  TOPICS_TOPIC: 'TOPICS_TOPIC',
  TOPICS_CONTENT: 'TOPICS_CONTENT',
  RECOMMENDED: 'RECOMMENDED',
  RECOMMENDED_POPULAR: 'RECOMMENDED_POPULAR',
  RECOMMENDED_RESUME: 'RECOMMENDED_RESUME',
  RECOMMENDED_NEXT_STEPS: 'RECOMMENDED_NEXT_STEPS',
  CONTENT_UNAVAILABLE: 'CONTENT_UNAVAILABLE',
  SEARCH: 'SEARCH',
  EXAM_LIST: 'EXAM_LIST',
  EXAM: 'EXAM',
  EXAM_ROOT: 'EXAM_ROOT',
  WAGE_DETAILS: 'WAGE_DETAILS',
};

// switch between modes
export const PageModes = {
  TOPICS: 'TOPICS',
  RECOMMENDED: 'RECOMMENDED',
  SEARCH: 'SEARCH',
  EXAM: 'EXAM',
  WAGE: 'WAGE',
};

export const ClassesPageNames = {
  ALL_CLASSES: 'ALL_CLASSES',
  CLASS_ASSIGNMENTS: 'CLASS_ASSIGNMENTS',
  LESSON_PLAYLIST: 'LESSON_PLAYLIST',
  CLASS_LEARNERS_LIST_VIEWER: 'CLASS_LEARNERS_LIST_VIEWER',
  EXAM_VIEWER: 'EXAM_VIEWER',
  EXAM_REPORT_VIEWER: 'EXAM_REPORT_VIEWER',
  LESSON_RESOURCE_VIEWER: 'LESSON_RESOURCE_VIEWER',
  ALL_NOTIFICATIONS: 'ALL_NOTIFICATIONS',
  MATCHUP_DETAILS: 'MATCHUP_DETAILS',
};

export const pageNameToModuleMap = {
  [ClassesPageNames.ALL_CLASSES]: 'classes',
  [ClassesPageNames.CLASS_ASSIGNMENTS]: 'classAssignments',
  [ClassesPageNames.EXAM_VIEWER]: 'examViewer',
  [ClassesPageNames.EXAM_REPORT_VIEWER]: 'examReportViewer',
  [ClassesPageNames.LESSON_PLAYLIST]: 'lessonPlaylist',
  [ClassesPageNames.LESSON_RESOURCE_VIEWER]: 'lessonPlaylist/resource',
  [ClassesPageNames.ALL_NOTIFICATIONS]: 'notifications',
  [ClassesPageNames.MATCHUP_DETAILS]: 'matchup',
  [PageNames.TOPICS_ROOT]: 'topicsRoot',
  [PageNames.RECOMMENDED]: 'recommended',
  [PageNames.TOPICS_CHANNEL]: 'topicsTree',
  [PageNames.TOPICS_CONTENT]: 'topicsTree',
  [PageNames.TOPICS_TOPIC]: 'topicsTree',
  [PageNames.RECOMMENDED_CONTENT]: 'topicsTree',
  [PageNames.WAGE_DETAILS]: 'wage',
};

export const LEARNER_ROLES = {
  MENTOR: 'Mentor',
  MENTEE: 'Mentee',
};

export const LEARNER_MATCHUP_TABLE_COLUMNS = {
  SUBJECT: 'subject',
  MENTOR: 'mentor',
  MENTEE: 'mentee',
  SUPERVISOR: 'supervisor',
};

export const ACTIVE_WAGE_TXN_STATUSES = ['COACH_APPROVED', 'CREATED'];

export const COMPLETED_WAGE_TXN_STATUSES = [
  'COMPLETED',
  'COACH_DENIED',
  'DENIED',
  'DENIED_INSUFFICIENT_FUND',
];

export const WAGE_TXN_TYPES = {
  CREDIT: 'CREDIT',
  DEBIT: 'DEBIT',
};
