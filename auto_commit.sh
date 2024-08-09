#!/bin/bash

# Set the start date
start_date="2021-05-14"
# Initialize the current date to the start date
current_date=$(date -d "$start_date" +%Y-%m-%d)

# Loop to create commits for 3 months (approximately 90 days)
while [[ $(date -d "$current_date" +%s) -le $(date -d "$start_date + 90 days" +%s) ]]
do
    # Randomly decide whether to make a commit (60% chance)
    commit_chance=$(shuf -i 1-100 -n 1)
    
    if [[ $commit_chance -le 60 ]]; then  # 60% chance to commit
        # Generate a random number of days (1, 2, or 3)
        random_days=$(shuf -i 1-3 -n 1)

        # Calculate the commit date
        commit_date="$current_date"

        # Generate a random hour and minute within the day
        random_hour=$(shuf -i 0-23 -n 1)
        random_minute=$(shuf -i 0-59 -n 1)

        # Format the random time
        random_time=$(printf "%02d:%02d:00" $random_hour $random_minute)

        # Create a new file or modify an existing file
        echo "Commit for date $commit_date at $random_time" > "file_$(date -d "$commit_date" +%Y%m%d_%H%M).txt"
        
        # Stage the file
        git add "file_$(date -d "$commit_date" +%Y%m%d_%H%M).txt"
        
        # Commit with the calculated date and random time
        GIT_COMMITTER_DATE="$commit_date $random_time" git commit -m "API update for $commit_date" --date "$commit_date $random_time"
    fi

    # Update the current date by adding the random number of days
    current_date=$(date -d "$current_date + $random_days days" +%Y-%m-%d)
done

echo "Commits created successfully!"
