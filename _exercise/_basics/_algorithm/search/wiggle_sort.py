# in-place sort array that nums[0] <= nums[1] >= nums[2] <= nums[3]....
# e.g., [3, 5, 2, 1, 6, 4] => [1, 6, 2, 5, 3, 4].

public void wiggleSort(int[] nums) {
    for (int i = 0; i < nums.length - 1; i++) {
        if ((i % 2 == 0) == (nums[i] > nums[i + 1])) {
            swap(nums, i, i + 1);
        }
    }
}
