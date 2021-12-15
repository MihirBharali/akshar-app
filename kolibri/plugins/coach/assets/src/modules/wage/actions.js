import { WageTransactionResource } from 'kolibri.resources';

export function createWageTransactionForLearnerRequest(
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
    getParams: { role: 'Coach', facility: facilityId },
  });
}

export function updateWageTransactionRequest(store, { data, facilityId }) {
  return WageTransactionResource.saveModel({
    data: data,
    getParams: { isBulkUpdate: 'true', facility: facilityId },
  });
}
