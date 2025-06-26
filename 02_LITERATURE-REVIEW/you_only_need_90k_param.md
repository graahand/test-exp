# You Only Need 90K Parameters to Adapt Light: a Light Weight Transformer for Image Enhancement and Exposure Correction

1. The paper addresses the common problem that images taken in difficult lighting conditions (too dark, too bright, under- or over-exposed) look bad and also **degrade the performance** of computer vision algorithms (like object detection).
2. Normally, a camera's internal **Image Signal Processor (ISP**) converts the raw sensor data into the standard image format (sRGB) we usually see. This process involves steps like **color correction** and adjusting brightness/contrast **(gamma correction).**
3. The researchers propose a new method called the **Illumination Adaptive Transformer (IAT).** Instead of just trying to fix the final image, IAT works by essentially **learning to *adjust the parameters of the ISP process itself* based on the input image**. It breaks down the ISP process and uses a Transformer model (specifically, attention queries) to figure out the **best adjustments** for things like color and gamma needed to correct the lighting.
4. The key advantages highlighted are that IAT is very small (lightweight, only **90k parameters**) and extremely fast (takes only **0.004 seconds per image**). Despite its efficiency, it performs better than current leading methods (State-Of-The-Art) on s**tandard tests for fixing low-light and exposure problems**. Importantly, fixing the images with IAT also significantly helps other computer vision tasks, like detecting objects or understanding image segments, perform better in these challenging lighting conditions.

**Notes from the Paper Text:**

- **Problem:** Real-world challenging illumination (low light, under/over-exposure) harms visual quality and computer vision task performance.
- **Background:** Cameras use an Image Signal Processor (ISP) to convert raw data to sRGB images, involving steps like color/gamma correction.
- **Proposed Solution:** Illumination Adaptive Transformer (IAT).
    - A lightweight and fast transformer model.
    - Aims to restore normally lit sRGB images from poorly lit inputs.
- **IAT Mechanism:**
    - Decomposes the ISP pipeline conceptually (into local/global components).
    - Uses attention queries to learn and adjust ISP-related parameters (e.g., color correction, gamma correction).
- **IAT Features:**
    - Very lightweight: ~90k parameters.
    - Very fast: ~0.004s processing time per image [inference time].
- **Performance:**
    - Consistently outperforms State-Of-The-Art (SOTA) methods on low-light enhancement and exposure correction benchmarks.
    - Significantly improves downstream tasks (object detection, semantic segmentation) under various lighting conditions.

---

---

## Content Based Image Retrieval

**Content-based image retrieval** (CBIR) is a process in image retrieval where the system searches for images based on their **visual and semantic content**, rather than **metadata or textual descriptions.** It involves extracting features from images, such as color, texture, and shape, and using these features to **compare and rank images in the database**. This technology is often used in applications like facial recognition, image search engines, and medical imaging.