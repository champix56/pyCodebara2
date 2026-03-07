IMAGE_IA_GEN_REST_URL="0.0.0.0:8000"
IMAGE_IA_GEN_ENDPOINT_GEN="/api/generate"
IMAGE_IA_GEN_ENDPOINT_METHOD="POST"
IMAGE_IA_GEN_BODY_BASE={
  "lcm_model_id": "stabilityai/sd-turbo",
  "openvino_lcm_model_id": "rupeshs/sd-turbo-openvino",
  "use_offline_model": False,
  "use_lcm_lora": False,
  "lcm_lora": {
    "base_model_id": "Lykon/dreamshaper-8",
    "lcm_lora_id": "latent-consistency/lcm-lora-sdv1-5"
  },
  "use_tiny_auto_encoder": False,
  "use_openvino": False,
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
  "use_seed": True,
  "use_safety_checker": False,
  "diffusion_task": "text_to_image",
  "lora": {
    "models_dir": "/home/champix/PycharmProjects/fastsdcpu/lora_models",
    "weight": 0.5,
    "fuse": True,
    "enabled": False
  },
  "controlnet": {
    "adapter_path": "string",
    "conditioning_scale": 0.5,
    "enabled": False
  },
  "dirs": {
    "controlnet": "/home/champix/PycharmProjects/fastsdcpu/controlnet_models",
    "lora": "/home/champix/PycharmProjects/fastsdcpu/lora_models"
  },
  "rebuild_pipeline": False,
  "rebuild_controlnet_pipeline": False,
  "use_gguf_model": False,
  "gguf_model": {
    "gguf_models": "/home/champix/PycharmProjects/fastsdcpu/models/gguf"
  }
}