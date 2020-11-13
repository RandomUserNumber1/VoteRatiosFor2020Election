# VoteRatiosFor2020Election
a reproduction of the vote ratios charts for the 2020 US Presidential Election - confirms that truncated data was used, and calculated vote ratios per batch are NOT accurate

Further explanation...

There is not sufficient precision in the vote share data (only 3 significant digits) in order to back-calculate accurate dem/rep ratios per batch. Please consider the following example, inspired by the Michigan data (but not an actual data point, I just wanted to make the numbers easier for myself).

Towards the tail end of the data there are over 5 million total votes. Let's call it 5.53 million. The republican share is 0.479 and the democrat share is 0.505. Since there are no actual vote totals for each party, just these ratios, so you have to estimate

rep votes = 5.53 mil x 0.479 = 2,648,870
dem votes = 5.53 mil x 0.505 = 2,792,650

For the sake of argument, let's say these are the true numbers at this point...
Now, let's say the next batch that comes in is for 10,000 votes, and it's 55% rep and 45% dem.

the total votes (true values) for each party is then
rep votes = 2,648,870 + 0.55 x 10,000 = 2,654,370
dem votes = 2,792,650 + 0.45 x 10,000 = 2,797,150
total votes = 5.54 million

The true ratios for each party is then
rep share = 2,654,370 / 5.54 mil = 0.479128...
dem share = 2,797,150 / 5.54 mil = 0.5049007...

The edison data would round these values to 3 significant digits
rep share = round(0.479128, 3) = 0.479
dem share = round(0.5049007, 3) = 0.505

No change in the overall share ratios even though the batch share was 0.55 rep vs 0.45 dem

Now since the overall share ratios have not changed, the apparent total vote counts for each party are
rep votes (apparent) = 0.479 x 5.54 mil = 2,653,660
dem votes (apparent) = 0.505 x 5.54 mil = 2,797,700

If you were to calculate the apparent dem/rep vote share for the batch, it would be no different than the overall vote share ratio of 0.505 / 0.479 =1.05, versus the true (and unknown) batch ratio of 0.45 / 0.55 = 0.82.

In summary, using the data in this manner is not appropriate, and you cannot make any conclusions from it.