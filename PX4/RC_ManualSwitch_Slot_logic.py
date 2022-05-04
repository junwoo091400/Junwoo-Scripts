import matplotlib.pyplot as plt

# Constants we need to calculate selected mode from the RC input
num_slots = 6
slot_width_half = 1/num_slots
slot_min = -1. - 0.05
slot_max = 1 + 0.05

def rcval_2_slotnum(rc_val):
    # Current Slot calculation logic in PX4 Autopilot master branch
    # rc_val comes in as [-1, 1] range

    # 1. Normalize the value and do some funky stuff
    rc_val_normalized_funky = ((rc_val - slot_min) * num_slots + slot_width_half) / (slot_max - slot_min)
    return (int)(rc_val_normalized_funky + slot_width_half + 1.)

# Another way of doing the mode switch in my opinion
def rcval_2_slotnum_junwoo(rc_val):
    # 1. normalize the value
    rc_val_normalized = (rc_val - slot_min) / (slot_max - slot_min)
    # 2. Multiplly by the channel number and add 1 to make selected mode start from 1
    channel_slot = (int)(rc_val_normalized * num_slots) + 1
    return channel_slot

### RC Val mode select test ###
rc_vals = [a/100. for a in range(-100, 101)]
print(rc_vals)

# Selected slots list for each RC values
slots_upstream = []
slots_junwoo = []

for rc_val in rc_vals:
    slot_select_upstream = rcval_2_slotnum(rc_val)
    slot_junwoo = rcval_2_slotnum_junwoo(rc_val)
    print('RC : {} | Slot upstream : {} | junwoo : {}'.format(rc_val, slot_select_upstream, slot_junwoo))
    slots_upstream.append(slot_select_upstream)
    slots_junwoo.append(slot_junwoo)

# Plot the RC Modes Selection
fig, ax = plt.subplots()

ax.plot(rc_vals, slots_upstream, 'r-', label='upstream')
ax.plot(rc_vals, slots_junwoo, 'b-', label='junwoo')

plt.legend() # Show the labels

# Mode change barriers with buffer zone (0.05)
rc_vals_barriers = [(((slot_max - slot_min)/num_slots) * i + slot_min) for i in range(1, num_slots+1)]
print(rc_vals_barriers)

# Mode change barriers with no buffer zone
rc_vals_barriers_groundtruth = [((2./num_slots) * i + -1.) for i in range(1, num_slots+1)]

ax.set_xticks(rc_vals_barriers, linestyle='--') # Vertical barriers visualization
ax.set_xticks(rc_vals_barriers_groundtruth, linestyle='*') # Vertical barriers visualization
ax.xaxis.grid(True)

plt.xlabel("RC Value")
plt.ylabel("Slot Selected")

plt.show()
