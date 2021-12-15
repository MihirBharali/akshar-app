import { WageTransactionResource } from 'kolibri.resources';

export function createWageRequestForLearner(
  store,
  { amount, requestType, reason, user_id, user_name, description, facilityId }
) {
  const request = {
    user_id: user_id,
    user_name: user_name,
    transaction_amount: amount,
    request_type: requestType,
    description: description,
    reason: reason,
  };
  return WageTransactionResource.saveModel({
    data: request,
    getParams: { role: 'Admin', facility: facilityId },
  });
}

export function updateWageRequestForLearners(store, { data, facilityId }) {
  return WageTransactionResource.saveModel({
    data: data,
    getParams: { isBulkUpdate: 'true', facilityId: facilityId },
  });
}

export function getTransactionsByDateRange(store, { startDate, endDate, facilityId }) {
  return WageTransactionResource.fetchCollection({
    getParams: {
      type: 'Reporting',
      status: 'COMPLETED',
      startDate: startDate,
      endDate: endDate,
      facility: facilityId,
    },
    force: true,
  });
}
