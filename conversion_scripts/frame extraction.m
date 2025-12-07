% ===========================
% Frame Extraction Script
% ===========================

% --- User-defined variables ---
full_file_path = "C:\Users\giuse\OneDrive\Desktop\IR+RGB cameras\test 1\IR video 1.mp4";
dest_path = "C:\Users\giuse\OneDrive\Desktop\extracted frames ir rgb cameras\test 1\IR camera";
frames_to_use = 140*4;             % Number of frames you want to extract
cam_type = "Primary";            % Camera type: 'Primary' or 'Secondary'
num_pair = 5;                    % If part of a camera pair

% --- Internal setup ---
flag_mis = 0;

try
    % Check if file exists
    if exist(full_file_path, 'file') ~= 2
        error('Video file not found at the specified path.');
    end

    % Create output folder if it doesn't exist
    if ~exist(dest_path, 'dir')
        mkdir(dest_path);
    end

    % for the rats put as duration 601, for the mouse 550
    % RGBVid1 5:00. IRVid1 3:30.
    % RGBVid2 4:59. IRVid2 3:59.
    % EXTRACT THE FIRST 1:30 MIN
    % RGB vid 15 frames. IR vid 60 frames
    % Total frames RGBVid1 15*300. Total frames IRVid1 60*210
    % Total frames RGBVid2 15*299. Total frames IRVid2 60*239
    % total frames to consider: RGB 15*90. IR 60*90
    % Open video 56.0768
    vidfile = VideoReader(full_file_path);
    total_frames = floor(56.0768 * 90);
    nskip = max(1, floor(total_frames / frames_to_use));

    k = 1;                     % Number of frames written
    frame_idx = 1;             % Index of current frame in video

    % Loop through video frames
    while hasFrame(vidfile)
        frame = readFrame(vidfile);

        % Save every nskip-th frame
        if mod(frame_idx, nskip) == 0 && k <= frames_to_use
            filename = sprintf('frame%04d.png', frame_idx);
            imwrite(frame, fullfile(dest_path, filename));

            % Display status message every 5 frames
            if mod(k, 5) == 0
                if strcmp(cam_type, 'Primary')
                    disp(['Writing calibration image ' num2str(k) ...
                          ' of ' num2str(frames_to_use) ...
                          ' for ' cam_type ...
                          (contains(dest_path, 'PrimarySecondary') ...
                           * [' of camera pair ' num2str(num_pair)])]);
                else
                    disp(['Writing calibration image ' num2str(k) ...
                          ' of ' num2str(frames_to_use) ...
                          ' for ' cam_type ' of camera pair ' num2str(num_pair)]);
                end
            end

            k = k + 1;
        end

        % Stop once desired number of frames is saved
        if k > frames_to_use
            break;
        end

        frame_idx = frame_idx + 1;
    end

    disp('✅ Frame extraction completed successfully.');

catch ME
    flag_mis = 1;
    msgbox('⚠️ Problem extracting frames. Please check your video path and try again.', 'Extraction Error');
    disp(getReport(ME));
end
