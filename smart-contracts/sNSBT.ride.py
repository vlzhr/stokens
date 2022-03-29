{-# STDLIB_VERSION 5 #-}
{-# CONTENT_TYPE DAPP #-}
{-# SCRIPT_TYPE ACCOUNT #-}

let nsbtId = base58'6nSpVyNH7yM69eg446wrQR94ipbbcmZMU1ENPwanC97g'
let snsbtId = base58'8wUmN9Y15f3JR4KZfE81XLXpkdgwnqoBNG6NmocZpKQx'
let isStopped = false

@Callable(i)
func stakeNSBT() = {
  let pmt = i.payments[0].value()
  let amount = pmt.amount
  if (pmt.assetId != nsbtId) then {
    throw("attach NSBT token only")
  } else if (isStopped) then { 
    throw("smart contract is on lock")
  } else {
    strict lockInv = invoke(Address(base58'3P8w8NXZUtYdCA13tHbDY5sW4mC27ZFJgG3'), "stake", [], [pmt])
    let snsbtIssue = Reissue(snsbtId, amount, true)
    [
      snsbtIssue,
      ScriptTransfer(i.caller, amount, snsbtId)
    ]
  }
}

@Verifier(tx)
func verify() = sigVerify(tx.bodyBytes, tx.proofs[0], tx.senderPublicKey)
        