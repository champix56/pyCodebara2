IMAGE_IA_GEN_REST_URL="0.0.0.0:8000"
IMAGE_IA_GEN_ENDPOINT_GEN="/api/gen"
IMAGE_IA_GEN_ENDPOINT_METHOD="POST"
IMAGE_IA_GEN_BODY_BASE={
  "lcm_model_id": "stabilityai/sd-turbo",
  "openvino_lcm_model_id": "rupeshs/sd-turbo-openvino",
  "use_offline_model": false,
  "use_lcm_lora": false,
  "lcm_lora": {
    "base_model_id": "Lykon/dreamshaper-8",
    "lcm_lora_id": "latent-consistency/lcm-lora-sdv1-5"
  },
  "use_tiny_auto_encoder": false,
  "use_openvino": false,
  "prompt": "",
  "negative_prompt": "",
  "init_image": "string",
  "strength": 0.6,
  "image_height": 512,
  "image_width": 512,
  "inference_steps": 1,
  "guidance_scale": 1,
  "clip_skip": 1,
  "token_merging": 0,
  "number_of_images": 1,
  "seed": 123123,
  "use_seed": false,
  "use_safety_checker": false,
  "diffusion_task": "text_to_image",
  "lora": {
    "models_dir": "/home/champix/PycharmProjects/fastsdcpu/lora_models",
    "weight": 0.5,
    "fuse": true,
    "enabled": false
  },
  "controlnet": {
    "adapter_path": "string",
    "conditioning_scale": 0.5,
    "enabled": false
  },
  "dirs": {
    "controlnet": "/home/champix/PycharmProjects/fastsdcpu/controlnet_models",
    "lora": "/home/champix/PycharmProjects/fastsdcpu/lora_models"
  },
  "rebuild_pipeline": false,
  "rebuild_controlnet_pipeline": false,
  "use_gguf_model": false,
  "gguf_model": {
    "gguf_models": "/home/champix/PycharmProjects/fastsdcpu/models/gguf"
  }
}