<template>

  <KModal
    :title="$tr('modalTitle')"
    :submitText="$tr('submitLabel')"
    :cancelText="$tr('cancelLabel')"
    @submit="$emit('submit', { 
      name: selectedLearner.label, 
      id: selectedLearner.value, 
      amount: amount, 
      requestType: requestType.value, 
      reason: reason.value,
      description: description })"
    @cancel="$emit('cancel')"
  >
    <KSelect
      v-model="selectedLearner"
      class="select"
      :label="$tr('learnerLabel')"
      :options="learnerOptions"
    />

    <KTextbox
      ref="amount"
      v-model="amount"
      type="number"
      :label="$tr('amountLabel')"
      :autofocus="false"
      :maxlength="maxLength"
      :max="maxAmount"
      :min="minAmount"
      :showInvalidText="true"
      :invalidText="invalidAmountValue"
      @blur="nameBlurred = true"
    />
    <KSelect
      v-model="requestType"
      class="select"
      :label="$tr('requestTypeLabel')"
      :options="requestTypeOptions"
    />
    <KSelect
      v-model="reason"
      class="select"
      :label="$tr('reasonLabel')"
      :options="reasonOptions"
    />
    <KTextbox
      ref="description"
      v-model="description"
      type="text"
      :label="$tr('descriptionLabel')"
      :autofocus="false"
      @blur="nameBlurred = true"
    />


  </KModal>

</template>
<script>

  import { mapState, mapGetters } from 'vuex';
  import {
    WageRequestOptions,
    WageRequestType,
    DefaultWageRequestType,
  } from 'kolibri.coreVue.vuex.constants';

  export default {
    name: 'CoachWageFormModal',
    data() {
      return {
        amount: 0,
        requestType: {},
        reason: {},
        selectedLearner: {},
        description: null,
        showMiscDescription: false,
      };
    },
    computed: {
      ...mapState('wage', ['coachWageRequests', 'learners']),
      maxLength() {
        return 4;
      },
      minAmount() {
        return 1;
      },
      maxAmount() {
        return 1000;
      },
      invalidAmountValue() {
        return this.$tr('invalidAmountError');
      },
      requestTypeOptions() {
        return Object.values(WageRequestType);
      },
      learnerOptions() {
        let learnersList = [];
        for (var i in this.learners) {
          const learner = this.learners[i];
          learnersList.push({ label: learner['full_name'], value: learner['id'] });
        }
        learnersList = learnersList.sort((a, b) => (a.label > b.label ? 1 : -1));
        return learnersList;
      },
      reasonOptions() {
        if (this.requestType.value == 'CREDIT') {
          return Object.values(WageRequestOptions.CREDIT);
        }
        return Object.values(WageRequestOptions.DEBIT);
      },
    },
    beforeMount() {
      this.init();
    },
    methods: {
      init() {
        this.requestType = DefaultWageRequestType;
      },
    },
    $trs: {
      modalTitle: 'New wage request',
      learnerLabel: 'Learner',
      submitLabel: 'Submit',
      cancelLabel: 'Cancel',
      amountLabel: 'Amount',
      requestTypeLabel: 'Request type',
      creditLabel: 'Credit',
      debitLabel: 'Debit',
      invalidAmountError: 'Invalid amount.',
      reasonLabel: 'Reason',
      mentoringLabel: 'Mentoring',
      gardeniningLabel: 'Gardening',
      carpentryLabel: 'Carpentry',
      onlinePurchaseLabel: 'Online purchase',
      cashWithdrawalLabel: 'Cash withdrawal',
      miscLabel: 'Miscellaneous',
      descriptionLabel: 'Description',
    },
  };

</script>
<style  lang="scss" scoped>

  .select {
    margin: 18px 0 36px;
  }

</style>
