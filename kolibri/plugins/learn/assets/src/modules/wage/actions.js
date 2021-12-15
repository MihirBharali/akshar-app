import { WageTransactionResource } from 'kolibri.resources';

export function createWageTransactionRequest(
  store,
  {
    amount,
    requestType,
    reason,
    description,
    user_id,
    user_name,
    coach_approver_id,
    coach_approver_name,
  }
) {
  const request = {
    user_id: user_id,
    user_name: user_name,
    created_by_id: user_id,
    created_by_name: user_name,
    coach_approver_id: coach_approver_id,
    coach_approver_name: coach_approver_name,
    transaction_amount: amount,
    request_type: requestType,
    reason: reason,
    description: description,
    status: 'CREATED',
  };
  return WageTransactionResource.saveModel({
    data: request,
  });
}
