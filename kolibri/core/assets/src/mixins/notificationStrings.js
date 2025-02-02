import { createTranslator } from 'kolibri.utils.i18n';

// TODO add error messages
export default createTranslator('NotificationStrings', {
  classCreated: {
    message: 'Class created',
    context: 'Adding a class',
  },
  classDeleted: {
    message: 'Class deleted',
    context: 'Deleting a class',
  },
  coachesAssignedNoCount: {
    message: '{count, plural, one {Coach assigned} other {Coaches assigned}}',
    context:
      'String appears as a short notification in a bottom left corner of the screen when more than one coach is assigned to a class, but without specifying the number.',
  },
  coachesRemovedNoCount: {
    message: '{count, plural, one {Coach removed} other {Coaches removed}}',
    context: 'Removing an unspecified number of coaches from a class',
  },
  learnersEnrolledNoCount: {
    message: '{count, plural, one {Learner enrolled} other {Learners enrolled}}',
    context: 'Enrolling an unspecified number of learners into group or class',
  },
  learnersRemovedNoCount: {
    message: '{count, plural, one {Learner removed} other {Learners removed}}',
    context: 'Removing (unenrolling) an unspecified number of learners from a group or class',
  },
  learnersEnrolledWithCount: {
    message: '{count, number} {count, plural, one {learner enrolled} other {learners enrolled}}',
    context: 'Enrolling a specified number of learners into group or class',
  },
  learnersRemovedWithCount: {
    message: '{count, number} {count, plural, one {learner removed} other {learners removed}}',
    context: 'Removing (unenrolling) a specified number of learners from a group or class',
  },
  userCreated: {
    message: 'User created',
    context: 'Creating a new user',
  },
  userDeleted: {
    message: 'User deleted',
    context: 'Deleting a user',
  },
  passwordReset: {
    message: 'Password reset',
    context:
      'Text will appear as a notification at the bottom after the user password has been reset',
  },
  changesSaved: {
    message: 'Changes saved',
    context: 'Generic message when something like a lesson, quiz, or user details has been changed',
  },
  lessonCreated: {
    message: 'Lesson created',
    context: 'Creating a new lesson',
  },
  lessonCopied: {
    message: 'Lesson copied',
    context: 'Copying a lesson to a classroom',
  },
  lessonDeleted: {
    message: 'Lesson deleted',
    context: 'Deleting a lesson',
  },
  resourcesAddedWithCount: {
    message: '{count, number} {count, plural, one {resource added} other {resources added}}',
    context: 'Adding a specified number of resources to a lesson',
  },
  resourcesRemovedWithCount: {
    message: '{count, number} {count, plural, one {resource removed} other {resources removed}}',
    context: 'Removing a specified number of resources from a lesson',
  },
  resourcesAddedNoCount: {
    message: '{count, plural, one {Resource added} other {Resources added}}',
    context: 'Adding an unspecified number of resources to a lesson',
  },
  resourcesRemovedNoCount: {
    message: '{count, plural, one {Resource removed} other {Resources removed}}',
    context: 'Removing an unspecified number of resources from a lesson',
  },
  resourceOrderSaved: {
    message: 'Resource order saved',
    context: 'Saving the new order of resources in a lesson',
  },
  quizCopied: {
    message: 'Quiz copied',
    context: 'Copying a quiz to a classroom',
  },
  quizCreated: {
    message: 'Quiz created',
    context: 'Text will appear as a notification at the bottom after the new quiz is created',
  },
  quizDeleted: {
    message: 'Quiz deleted',
    context: 'Deleting a quiz',
  },
  groupCreated: {
    message: 'Group created',
    context: 'Creating a new learner group',
  },
  groupDeleted: {
    message: 'Group deleted',
    context: 'Deleting a learner group',
  },
  learnerRecommendedForPromotion: {
    message:
      '{count, number} {count, plural, one {student recommended for promotion} other {students recommended for promotion}}',
    context: 'Recommending a specified number of learner for promotion',
  },
  learnerApprovedForPromotion: {
    message:
      '{count, number} {count, plural, one {student approved for promotion} other {students approved for promotion}}',
    context: 'Approving a specified number of learner for promotion',
  },
  learnerDeniedForPromotion: {
    message:
      '{count, number} {count, plural, one {student denied promotion} other {students denied promotion}}',
    context: 'Denying a specified number of learner for promotion',
  },
  wageTxnCreatedSuccessMessage: {
    message: 'Request raised successfully.',
    context: 'Successfully raising a wage credit/debit requests',
  },
  wageTxnUpdatedSuccessMessage: {
    message: 'Transaction updated successfully.',
    context: 'Successfully updating a wage credit/debit requests',

  },
  // TODO move more messages into this namespace:
  // - "Quiz started"
  // - "Quiz Ended"
  // - "Quiz report is not visible to learners"
  // - "Quiz report is visible to learners
  // - "Lesson is visible to learners"
  // - "Lesson is not visible to learners"
});
