// IIRCoeffs : coefficients (b0, b1, b2, a0, a1, a2) for N_SOS_SECTIONS cascaded SOS sections
#define IIR_QXY_RES_NBITS 13 // Q2.13
#define N_SOS_SECTIONS 4
int32_t IIRCoeffs_Q2_5[N_SOS_SECTIONS][6] = {
{27,-52,27,32,-59,31},
{32,-61,32,32,-60,31},
{32,-61,32,32,-60,32},
{32,-61,32,32,-61,32},
};
int32_t IIRu[N_SOS_SECTIONS] = {0}, IIRv[N_SOS_SECTIONS] = {0};
