const ALL = 'All';
const ACTIVE = 'Active';
const ACTIVE_WAGE_TXN_STATUSES = ['COACH_APPROVED', 'CREATED'];

const COMPLETED_WAGE_TXN_STATUSES = [
  'COMPLETED',
  'COACH_DENIED',
  'DENIED',
  'DENIED_INSUFFICIENT_FUND',
];

export default function filterTransactionsByStatusType(transactions, filterType) {
  if (filterType === ALL) {
    return transactions;
  }
  const filterToApply =
    filterType === ACTIVE ? ACTIVE_WAGE_TXN_STATUSES : COMPLETED_WAGE_TXN_STATUSES;
  return transactions.filter(item => filterToApply.includes(item['status']));
}
