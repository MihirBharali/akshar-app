<template>

  <KModal
    :title="$tr('modalTitle')"
    :submitText="$tr('submitLabel')"
    :cancelText="$tr('cancelLabel')"
    @submit="$emit('submit', {
      amount: amount,
      requestType: requestType.value,
      reason: reason.value,
      description: description,
      supervisor: supervisor,
    })"
    @cancel="$emit('cancel')"
  >
    <KTextbox
      ref="amount"
      v-model="amount"
      type="number"
      :label="$tr('amountLabel')"
      :autofocus="true"
      :maxlength="maxLength"
      :max="maxAmount"
      :min="minAmount"
      :showInvalidText="true"
      :invalidText="invalidAmountValue"
      @blur="nameBlurred = true"
    />
    <KSelect
      v-model="supervisor"
      class="select"
      :label="$tr('supervisorLabel')"
      :options="supervisorOptions"
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

  import {
    WageRequestOptions,
    WageRequestType,
    DefaultWageRequestType,
  } from 'kolibri.coreVue.vuex.constants';

  export default {
    name: 'LearnerWageFormModal',
    props: {
      supervisors: {
        type: Array,
        required: true,
      },
    },
    data() {
      return {
        amount: 0,
        requestType: {},
        reason: {},
        description: null,
        supervisor: {},
      };
    },
    computed: {
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
      reasonOptions() {
        if (this.requestType.value == 'CREDIT') {
          return Object.values(WageRequestOptions.CREDIT);
        }
        return Object.values(WageRequestOptions.DEBIT);
      },
      supervisorOptions() {
        let supervisorsList = [];
        for (var i in this.supervisors) {
          const supervisor = this.supervisors[i];
          supervisorsList.push({ label: supervisor['full_name'], value: supervisor['id'] });
        }
        return supervisorsList;
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
      supervisorLabel: 'Teacher',
    },
  };

</script>
<style  lang="scss" scoped>

  .select {
    margin: 18px 0 36px;
  }

</style>
