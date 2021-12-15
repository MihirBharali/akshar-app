import { WageAccountResource, WageTransactionResource } from 'kolibri.resources';
import { PageNames } from '../../constants';

export function showWageAccountDetailsPage(store) {
  const facilityId = store.getters.currentFacilityId;
  return store.dispatch('loading').then(() => {
    return WageAccountResource.fetchModel({
      id: store.getters.currentUserId,
      getParams: {
        getTransactions: true,
        getSupervisors: true,
        facility: facilityId,
      },
    })
      .then(details => {
        store.commit('wage/SET_LEARNER_WAGE_DETAILS', details);
        store.commit('SET_PAGE_NAME', PageNames.WAGE_DETAILS);
        store.dispatch('notLoading');
      })
      .catch(error => {
        if (error.response.status == 404) {
          // if account is not found, create one for the logged in learner
          return createWageAccount(store);
        }
        store.dispatch('handleApiError', error);
        // Allows triggering of AuthMessage.vue
        return store.dispatch('handleError', error);
      });
  });
}

export function createWageAccount(store) {
  const request = { user: store.getters.currentUserId, userType: 'LEARNER' };
  return WageAccountResource.saveModel({
    data: request,
  })
    .then(() => {
      showWageAccountDetailsPage(store);
    })
    .catch(error => {
      store.dispatch('handleApiError', error);
    });
}
